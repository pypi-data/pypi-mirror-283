import pandas as pd
import numpy as np  
import scipy 
import matplotlib.colors as mcolors 
import warnings 
from matplotlib.ticker import ScalarFormatter
import matplotlib.pyplot as plt 

customColorList = [ mcolors.XKCD_COLORS[f"xkcd:{a}"] for a in ["bright blue","bright red","apple green",'yellow orange',
                                                               "blueberry","blood red","asparagus","amber",
                                                               "bright sky blue","brick orange","acid green","brownish yellow",
                                                               "amethyst","apricot","barbie pink","burgundy"]]


class trashPandas(pd.DataFrame):
    def __init__(self,df=pd.DataFrame(),*args,**kwargs):
        """
        Initializes the trashPandas object.

        Parameters:
        - df (pd.DataFrame): The input DataFrame.
        - args: Additional positional arguments.
        - kwargs: Additional keyword arguments.

        Returns:
        None
        """
        super().__init__(data=df.values,columns=df.columns, **kwargs)
        
        #Pandas does not like it too much when I 
        #create items using the self.itm = syntax 
        #so I blocked warnings here 
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.scale = 1
            self.PSD = None
            self.column_units = dict() 
            self.dt = -1 
            self.peaks = dict()
            self.decrease = dict()
            self.name = "unspecified name"
            self.PSD = pd.DataFrame()
            self.FFT = pd.DataFrame()
            self.crossings = dict()
            self.downCrossings = dict()
            self.cycles = dict()
            self.infos = dict()

    #####################################################################################################
    #####################################################################################################
    ###                                      Signal processing                                        ###
    #####################################################################################################
    #####################################################################################################

    def getDt(self):
        """
        Reads the sampling period in the OpenFAST data and returns it.

        Returns:
            float: The sampling period of the OpenFAST data.
        """
        if 'Time' not in self.columns:
            raise ValueError("The 'Time' column does not exist in the DataFrame.")
        
        if self.dt <= 0:
            time = np.array(self['Time'])
            self.dt = np.mean(time[1:] - time[0:-1])
            return self.dt
        else:
            return self.dt

    def reboundTimeWindow(self,tWindow) :
        """
        If the timeWindow [t1,t2] is bigger than the available time, automatically resize it to the available time.

        Parameters:
        - tWindow (list): The time window specified as [t1, t2].

        Returns:
        list: The rebounded time window.
        """
        if tWindow[0] == 0 :
            tWindow[0] = self.Time.values[0]
        if tWindow[1] == -1 : 
            tWindow[1] = self.Time.values[-1]
        return tWindow 
    
    def timeWindow(self,window) :
        """
        Selects a time window in the dataframe and removes values outside the window.

        Parameters:
        - window: Can either be specified as a tStart float or as a [tStart, tEnd] list.

        Returns:
        None
        """
        self.selectTimeWindow(window)

    def selectTimeWindow(self, window):
        """
        Selects a time window in the dataframe and removes values outside the window.

        Parameters:
        - window: Can either be specified as a tStart float or as a [tStart, tEnd] list.

        Returns:
        None
        """
        if not isinstance(window, list):
            tS = window
            tE = self['Time'].tail(1).to_list()[0]
        else:
            tS, tE = window
        if tE == -1:
            tE = self['Time'].values[-1]
        self = self.drop(self.index[(self['Time'] < tS)].to_list() +
                         self.index[(self['Time'] > tE)].to_list(),
                         inplace=True)

    def linComColumns(self,coeffs,columns,newName):
        """
        Perform linear combination of columns.

        Args:
            coeffs (list): List of coefficients for the linear combination.
            columns (list): List of column names to be combined.
            newName (str): Name of the new column.

        Returns:
            None
        """
        self.linearCombinationColumns(coeffs,columns,newName)

    def linearCombinationColumns(self, coeffs, columns, newName):
        """
        Perform linear combination of columns.

        Args:
            coeffs (list): List of coefficients for the linear combination.
            columns (list): List of column names to be combined.
            newName (str): Name of the new column.

        Returns:
            None
        """
        self[newName] = 0 
        for (i,c) in enumerate(coeffs) :
            self[newName] = self[newName]+c*self[columns[i]]

    def transferMatrix(self,inChannel,conversionMatrix,outChannels=None):
        """
        Apply a transfer matrix to create columns that the values of the former ones are in the new base.

        Parameters:
        - inChannel: The variables to be changed to mode base.
        - outChannel: Name for the output channels, default is "Mode_[n]".
        - conversionMatrix: len()*len() np array.

        Returns:
        None
        """
        if type(outChannels)==type(None) : 
            outChannels = [f"Mode{i+1}" for i in range(len(inChannel))]
        outChannelsTEMP = [f"{outChannel}_TEMP" for outChannel in outChannels] 
        for (i,outChannel) in enumerate(outChannelsTEMP):
            coeffs = conversionMatrix[i]
            self.linComColumns(coeffs,inChannel,outChannel)
        for (i,outChannel) in enumerate(outChannels):
            self[outChannel] = self[outChannelsTEMP[i]]
            self.drop(labels = outChannelsTEMP[i],axis = 1,inplace=True)

    def computePSD(self,columns="all",nperseg=None,normalize=False,tWindow=[0,-1]):
        """
        Computes the power spectral density using welch method from scipy.

        Parameters:
        - columns: The columns to compute the PSD for. Default is "all".
        - nperseg: The length of each segment. Default is None.
        - normalize: Whether to normalize the PSD. Default is False.
        - tWindow: The time window to compute the PSD for. Default is [0, -1].

        Returns:
        None
        """
        tWindow = self.reboundTimeWindow(tWindow)
        if isinstance(columns,str) :
            columns = self.columns 
        fs = 1/self.getDt()
        for col in columns : 
            data = (self[(self.Time >= tWindow[0]) & (self.Time <= tWindow[1]) ])[col].interpolate()
            
            if nperseg is not None : 
                if nperseg >= data.shape[0] : 
                    nperseg = data.shape[0]
            
            self.PSD['f'],self.PSD[col] = scipy.signal.welch(data,fs=fs,nperseg=nperseg)
            if normalize : 
                self.PSD[col] =self.PSD[col]/ self.PSD[col].sum()

    def computeFFT(self,columns="all",normalize=False,tWindow=[0,-1]):
        """
        Computes the fourier transform using scipy fft.

        Parameters:
        - columns: The columns to compute the FFT for. Default is "all".
        - normalize: Whether to normalize the FFT. Default is False.
        - tWindow: The time window to compute the FFT for. Default is [0, -1].

        Returns:
        None
        """
        tWindow = self.reboundTimeWindow(tWindow)
        if isinstance(columns,str) :
            columns = self.columns 
        fs = 1/self.getDt()
        for col in columns : 
            if col not in self.FFT.columns : 
                data = (self[(self.Time >= tWindow[0]) & (self.Time <= tWindow[1]) ])[col].interpolate()
                N = data.size 
                self.FFT['f'] = scipy.fft.fftfreq(N,self.getDt())[:N//2]
                self.FFT[col] = abs(scipy.fft.fft(data.to_numpy())[:N//2])

    def rmOffset(self,columns,timeWindow=[0,-1]) :
        """
        Remove the mean computed over "timeWindow" from the desired columns.

        Parameters:
        - columns: The columns to remove the mean from.
        - timeWindow: The time window to compute the mean over. Default is [0, -1].

        Returns:
        None
        """
        if not isinstance(columns,list) :
            columns = [columns]
        timeWindow = self.reboundTimeWindow(timeWindow)
        for col in columns : 
            moy = (self[(self.Time>=timeWindow[0]) & (self.Time <= timeWindow[1])])[col].mean()
            self[col] = self[col] - moy 

    def slideTime(self,DeltaT) :
        """
        Adds an offset DeltaT to the time column.

        Parameters:
        - DeltaT: The offset to add to the time column.

        Returns:
        None
        """
        self['Time'] = self['Time'] + DeltaT 

    def getPeaks(self,column,timeWindow=[0,-1],distT=0.1,**kwargs):
        """
        Find all the peaks in a signal, the minimum distance between two peaks is distT.

        Parameters:
        - column: The column to find peaks in.
        - timeWindow: The time window to find peaks in. Default is [0, -1].
        - distT: The minimum distance between two peaks. Default is 0.1.
        - kwargs: Additional keyword arguments.

        Returns:
        None
        """
        if 'distance' in list(kwargs.keys()) :
            distance = kwargs['distance']
        else :  
            distance = int(distT/self.getDt())
        timeWindow = self.reboundTimeWindow(timeWindow)
        time = (self[(self.Time >= timeWindow[0]) & (self.Time <= timeWindow[1]) ])['Time'].interpolate()
        signal = (self[(self.Time >= timeWindow[0]) & (self.Time <= timeWindow[1]) ])[column].interpolate()
        time.reset_index(drop=True,inplace=True)
        signal.reset_index(drop=True,inplace=True)
        index = list(scipy.signal.find_peaks(signal,distance=distance)[0])
        peaks = np.stack((time[index],signal[index]),axis=1)
        self.peaks[column] = peaks

    def getDecrease(self,column,timeWindow=[0,-1],**kwargs) :
        """
        For a damped signal, gets the time of each peaks, the amplitude and the decrement for each peak.

        Parameters:
        - column: The column to find peaks in.
        - timeWindow: The time window to find peaks in. Default is [0, -1].
        - kwargs: Additional keyword arguments.

        Returns:
        None
        """
        self.getPeaks(column,timeWindow,**kwargs)
        peaks = self.peaks[column]
        time = peaks[:,0]
        signal = peaks[:,1]
        dTime = (time[1:]+time[:-1])/2
        decrease = signal[:-1]-signal[1:]
        amplitudes = (signal[1:]+signal[:-1])/2
        self.decrease[column] = np.stack((dTime,amplitudes,decrease),axis=1)

    def sample(self,N) :
        """
        Keeps one in every n row.

        Parameters:
        - N: The sampling rate.

        Returns:
        None
        """
        self = self.iloc[::N]

    def perfectFilter(self,column,fIn,fOut=-1) :
        """
        Apply FFT and reverse FFT to perform perfect filtering.

        Parameters:
        - column: The column to perform filtering on.
        - fIn: The lower frequency limit.
        - fOut: The upper frequency limit. Default is -1.

        Returns:
        numpy.ndarray: The filtered signal.
        """
        if isinstance(fIn,list) : 
            if len(fIn)==2 : 
                fIn,fOut = fIn 
        signal = self[column].values  
        N = signal.size
        signal_fft = scipy.fft.fft(signal)
        freq = scipy.fft.fftfreq(N, d=self.getDt())
        if fOut == -1:  # If fOut is -1, set fOut to infinity
            fOut = np.inf
        mask = (np.abs(freq) >= fIn) & (np.abs(freq) <= fOut)
        filtered_fft = signal_fft * mask
        filtered_signal = scipy.fft.ifft(filtered_fft)
        return np.real(filtered_signal)

    def detectCrossing(self,column,filter=None) :
        """
        Detects every time the curve cuts the zero line.

        Parameters:
        - column: The column to detect crossings in.
        - filter: The frequency filter range. Default is None.

        Returns:
        None
        """
        if filter is not None :
            fIn,fOut = filter 
            signal = self.perfectFilter(column,fIn,fOut) 
        else : 
            signal = self[column].values 
        time = self['Time'].values 
        signs = np.sign(signal)
        signChanges = signs[:-1]*signs[1:]
        idxCrossings = np.nonzero(signChanges <0)
        tCrossings = time[idxCrossings]
        vCrossings = signal[idxCrossings]
        idxCrossings = idxCrossings[0]
        #Up or down crossing 
        self.crossings[column] = np.stack((idxCrossings,tCrossings,vCrossings),axis=1)
        # Down crossing 
        Dindexes = np.nonzero(vCrossings > 0 )
        idxDCrossings = idxCrossings[Dindexes]
        tDCrossings = tCrossings[Dindexes]
        vDCrossings = vCrossings[Dindexes]
        self.downCrossings[column] = np.stack((idxDCrossings,tDCrossings,vDCrossings),axis=1)

    def detectCycles(self, column, filter=None):
        """
        Read the amplitude and period of the signal based on down crossing cycle detection.
        
        Args:
            column (str): The name of the column to analyze.
            filter (optional): A filter to apply to the data before analysis.
        
        Returns:
            pandas.DataFrame: A DataFrame with cycle information, including start and end indices, start and end times,
            duration, minimum, and maximum values for each cycle.
        """
        self.detectCrossing(column, filter)
        cycles = dict()
        idx, times, amps = np.split(self.downCrossings[column], [1, 2], axis=1)
        idx = idx.flatten()
        times = times.flatten()
        cycles["Duration"] = -times[:-1] + times[1:]
        cycles["tStart"] = times[:-1]
        cycles["tEnd"] = times[1:]
        cycles["startIndex"] = idx[:-1]
        cycles["endIndex"] = idx[1:]
        cMin = [np.min(self[column].values[int(idx[i]):int(idx[i + 1])]) for i in range(idx.size - 1)]
        cMax = [np.max(self[column].values[int(idx[i]):int(idx[i + 1])]) for i in range(idx.size - 1)]
        cycles["Min"] = cMin
        cycles["Max"] = cMax
        self.cycles[column] = pd.DataFrame.from_dict(cycles)
    
    def coherence(self,columnA,columnB,lowFreq=0.025) : 
        x = self[columnA]
        y = self[columnB]
        fs = 1/self.getDt()
        nperseg = np.floor(fs/lowFreq)+1
        coherence = scipy.signal.coherence(x, y, fs=fs,nperseg=nperseg)
        return(coherence) 

    def crossSpectralDensity(self,columnA,columnB,lowFreq=0.025) : 
        x = self[columnA]
        y = self[columnB]
        fs = 1/self.getDt()
        nperseg = np.floor(fs/lowFreq)+1
        csd = scipy.signal.csd(x, y, fs=fs,nperseg=nperseg)
        return(csd)

    def autoSpectralDensity(self,columnA,lowFreq=0.025) :
        x = self[columnA]
        fs = 1/self.getDt()
        nperseg = np.floor(fs/lowFreq)+1
        # print(f"\n nperseg is {nperseg} \n")
        asd = scipy.signal.welch(x,fs=fs,nperseg=nperseg)
        return(asd)


    #####################################################################################################
    #####################################################################################################
    ###                                      Formating the data                                        ###
    #####################################################################################################
    #####################################################################################################
    def getOpenFASTUnits(self):
        """ Alias for getColumnUnits, deprecated"""
        self.getColumnUnits()

    def getColumnUnits(self):
        """
        Retrieves the units of each column in the DataFrame.

        Returns:
            dict: A dictionary where the keys are the column names and the values are the corresponding units.
        """
        column_units = {}
        for col in self.columns:
            if '_' in col:
                name, *_, unit = col.split('_')
                column_units[name] = unit.replace("[", "").replace("]", "")
        self.column_units = column_units

    def shortenColNames(self):
        """
        Shortens the column names by removing the part after the underscore.
        """
        if not self.column_units:
            self.getColumnUnits()
        self.columns = [col.split('_')[0] for col in self.columns]
    
    def SIUnits(self):
        "Changes all the units to SI units "
        for col in self.columns:
            factor = 1
            match self.column_units[col]:
                case "kN":
                    [newUnit, factor] = ["N", 1000]
                case "kN/s":
                    [newUnit, factor] = ["N/s", 1000]
                case "MN":
                    [newUnit, factor] = ["N", 1000000]
                case "MN":
                    [newUnit, factor] = ["N", 1000000]
                case "kN-m":
                    [newUnit, factor] = ["N-m", 1000]
                case "kW":
                    [newUnit, factor] = ["W", 1000]
            if factor != 1 :        
                self.column_units[col], self[col] = newUnit, factor * self[col]
    def anglesInDeg(self) :
        """If the units of the angles in the columns are "rad", sets them to deg """

        for col in self.columns :
            if self.column_units[col] == "rad" :
                self.column_units[col] == "deg"
                self[col] = 180/np.pi*self[col]
            if self.column_units[col] == "rad/s" :
                self.column_units[col] == "deg/s"
                self[col] = 180/np.pi*self[col]

    def froudeScale(self,cols='all',scale=1) :
        """
        Goes through the columns and set them to scale according to Froude scaling law using the units to get the scaling factor 

        possibility to specify scale as a [lambda,mu] tuple,
        by default mu will be set to 1 
        """
        if hasattr(scale, '__len__'):
            if len(scale) != 2 : 
                raise(Error)
            else :
                raise("Mu is not yet taken into account")
                (landa,mu) = scale 
        else : 
            (landa,mu) = (scale,1)
        
        if  isinstance(cols,list) :
            pass 
        elif isinstance(cols,str) :
            if cols == 'all':
                cols = list(self.columns)
            else : 
                raise("Unrecognised column string")
        #Remove doubel items in columns 
        cols = list(set(cols))
        for col in cols : 
            self[col] = self[col]/getFroudeFactor(landa,
                                              self.column_units[col])
        self.scale = landa

 #####################################################################################################
    #####################################################################################################
    ###                                       Plotting section                                        ###
    #####################################################################################################
    #####################################################################################################

    """Functions defined after this line are dedicated to plotting features of the trashpandas """


    def customPlot(self,X,Y,ax=None,**kwargs) :
        """
        Baseline xy plot for trashpandas 

        key word arguments : 
        timeWindow : a list of [t1,t2]
        color : a matplotlib color or the index of a color in my custom color palette 
        linewdith : for the plot 
        """
        if ax == None : 
            fig, ax = plt.subplots(1,1)
        
        if 'color'  in kwargs : 
            color = kwargs.get('color')
            if isinstance(color,int) :
                color = customColorList[color]
            elif isinstance(color,str) :
                pass 
            else : 
                raise("The kwarg color was not read properly")
        else : 
            color = customColorList[0]

        if 'lineWidth' in kwargs : 
            linewidth = kwargs.get("linewidth") 
        else :
            linewidth =  0.6

        if 'timeWindow' in kwargs :
            timeWindow = kwargs.get('timeWindow') 
        else : 
            timeWindow = [np.min(X),np.max(X)] 
        
        if timeWindow[0] == 0 :
            timeWindow[0] = np.min(X)
        if timeWindow[1] == -1 :
            timeWindow[1] = np.max(X)
        if 'xlabel' in kwargs : 
            xlabel = kwargs.get("xlabel")
        else : 
            xlabel = 'unspecified'
        if 'ylabel' in kwargs : 
            ylabel = kwargs.get("ylabel")
        else : 
            ylabel = 'unspecified'
        if 'label' in kwargs : 
                    label = kwargs.get("label")
        else : 
            label = self.name


        ax.plot(X,
                Y, 
                label=label,
                color=color,
                linewidth=linewidth)
        ax.tick_params(labelbottom=True)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_xlim(timeWindow)
        ax.grid(True)

        if 'xscale' in kwargs :
            ax.set_xscale(kwargs.get("xscale"))
        if 'yscale' in kwargs :
            ax.set_yscale(kwargs.get("yscale"))
             




    def plotTS(self,column,ax=None,**kwargs)  :
        """Plot a time series of desired serie on desired ax"""
        X = self['Time'] 
        if column in self.columns :
            Y = self[column]
        else :
            Y = np.zeros(X.size)
        xlabel = "Time (s)"
        unit = self.column_units.get(column,"-")
        ylabel = f"{column} ({unit})"
        self.customPlot(X,Y,ax=ax
                        ,xlabel=xlabel,ylabel=ylabel
                        ,**kwargs)


    def plotPSD(self,column,ax=None ,PSDZoom=1,**kwargs) :
        """Plot a PSD on a desired axis """
        if 'xScale' in kwargs.keys() :
            xScale = kwargs['xScale']
        else  : xScale = 'log'  
        if 'yScale' in kwargs.keys() :
            yScale = kwargs['yScale']
        else  : yScale = 'log'   
        axPSD = ax
        X= self.PSD['f']
        Y = self.PSD[column]
        timeWindow = [X[1],max(X)/PSDZoom]
        
        self.customPlot(X,Y,ax=ax,
                        xlabel = "Freq (Hz)",
                        ylabel = f"{column} ({self.column_units.get(column,'-')})^2/Hz)",
                        xscale=xScale,
                        yscale=yScale,
                        timeWindow = timeWindow,
                        **kwargs)
        
        #set the x ticks in normal writing not scientif 
        ax.xaxis.set_major_formatter(ScalarFormatter())
        ax.xaxis.get_major_formatter().set_scientific(False)
        ax.xaxis.get_major_formatter().set_useOffset(False)

    def plotFFT(self,column,ax=None ,PSDZoom=1,**kwargs) :
        """Plot a PSD on a desired axis """
        axPSD = ax
        X= self.FFT['f']
        Y = self.FFT[column]
        timeWindow = [X[1],max(X)/PSDZoom]
        self.customPlot(X,Y,ax=ax,
                        xlabel = "Freq (Hz)",
                        ylabel = f"{column} ({self.column_units.get(column,'-')}))",
                        xscale='log',
                        yscale='log',
                        timeWindow = timeWindow,
                        **kwargs)

    def boxPlot(self,column,ax=None,xpos=1,**kwargs) : 
        """Plot a custom shape of boxplot (box at 1st and 9th decile )
        and whiskers to min and max. Please avoid confusion with pandas.df.boxplot
        """
        if ax == None : 
            fig, ax = plt.subplots(1,1)
        
        if "filter" in kwargs.keys() :
            filter = kwargs.pop("filter")
            data = self.perfectFilter(column,filter)
        else : 
            filter = [0,1]
            data = self[column].values
        
        if "timeWindow" in kwargs.keys() :
            timeWindow = kwargs.pop("timeWindow")
            tS,tE = self.reboundTimeWindow(timeWindow)
            idx = self.index[(self['Time'] < tS)].to_list() + self.index[(self['Time'] > tE)].to_list()
            data = np.delete(data,idx)

        mean = np.mean(data)
        tenth_decile = np.percentile(data, 10)
        ninetieth_decile = np.percentile(data, 90)
        minimum = np.min(data)
        maximum = np.max(data)
        # Draw the box
        ax.plot([xpos-0.3, xpos+0.3], [tenth_decile, tenth_decile], **kwargs)
        ax.plot([xpos-0.3, xpos+0.3], [ninetieth_decile, ninetieth_decile], **kwargs)
        ax.plot([xpos-0.3, xpos-0.3], [tenth_decile, ninetieth_decile], **kwargs)
        ax.plot([xpos+0.3, xpos+0.3], [tenth_decile, ninetieth_decile], **kwargs)
        
        # Draw the median line
        ax.plot([xpos-0.3, xpos+0.3], [mean, mean], **kwargs)
        
        # Draw the whiskers
        ax.plot([xpos, xpos], [minimum, tenth_decile], **kwargs)
        ax.plot([xpos, xpos], [ninetieth_decile, maximum], **kwargs)
        ax.plot([xpos-0.15, xpos+0.15], [minimum, minimum], **kwargs)
        ax.plot([xpos-0.15, xpos+0.15], [maximum, maximum], **kwargs)
        
        # Add label
        # ax.text(xpos, minimum - 2*(maximum-minimum)/20, self.name, ha='center')
        # ax.set_xticks([])
        ax.set_xticks([xpos], [self.name])
# for minor ticks
        # ax.set_xticks([], minor=True)
        unit = self.column_units.get(column,"-")
        ylabel = f"{column} ({unit})"
        ax.set_ylabel(ylabel)



    #####################################################################################################
    #####################################################################################################
    ###                                      Running test                                        ###
    #####################################################################################################
    #####################################################################################################



if __name__ == '__main__':
    print('This is the trashPandas class. It is a subclass of the pandas.DataFrame class.')
    time = np.arange(-20, 260, 0.02)

    f1 = 1/3
    f2 = 1/10 
    f3 = 1/50 
    signal1 = 0.5 + np.sin(2 * np.pi * f1 * time) + np.sin(2 * np.pi * f2 * time) + np.sin(2 * np.pi * f3 * time)
    noise1 = np.random.normal(0, 0.1, len(time))
    signal_with_noise1 = signal1 + noise1

    f1 = 1/3
    f2 = 1/12 
    f3 = 1/30 
    signal2 = -0.3 + np.sin(2 * np.pi * f1 * time) + np.sin(2 * np.pi * f2 * time) + np.sin(2 * np.pi * f3 * time)
    noise2 = np.random.normal(0, 0.1, len(time))
    signal_with_noise2 = signal2 + noise2

    signal_with_noise3 = np.sin(2 * np.pi * (1/20) * time)

    df = trashPandas()
    df['Time_[s]'] = time
    df['Speed_[m/s]'] = signal_with_noise1
    df['Load_[kN]'] = signal_with_noise2
    df['Pitch_[rad]'] = np.sin(2 * np.pi * (1/20) * time)
    df.name = 'Test'

    fig,axs = plt.subplots(4,1,figsize=(6,6),sharex=True)
    axi = axs[1]
    
    df.getColumnUnits()
    df.shortenColNames()
    df.SIUnits()
    df.anglesInDeg()

    df.plotTS('Speed', ax=axs[0], color='blue')
    # df.plotTS('Load', ax=axs[0], color='red')
    df.plotTS('Pitch', ax=axs[0], color='green')

    df.rmOffset('Speed')
    df['Speed_filtered']=df.perfectFilter('Speed', [0, 9])
    df.plotTS('Speed_filtered',ax=axs[1],linestyle='--')

    df.computePSD('Speed') 
    df.computePSD('Speed_filtered')
    df.plotPSD('Speed',ax=axs[2],xScale='linear')
    df.plotPSD('Speed_filtered',ax=axs[2],xScale='linear',linestyle='--')
    for ax in axs : ax.legend()
    plt.tight_layout()
    plt.show()
    

