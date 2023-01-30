"""

try:
    import serial.tools.list_ports
    for port in serial.tools.list_ports.comports():
        port_parse = str(port).split(' ')
        if 'Isolated' in port_parse and 'RS-485' in port_parse:
            _fan_port = int(port_parse[0][-1])
except Exception:
    pass

defaults_by_cmd = { # 'field':None indicates field is required when assembling command

    'initialize':('INITIALIZE', {
        'initializeAlways':0
    
 }),
    'ConnectUsingIP':('MPE_CONNECT', {
        'ipAddress':'',                  # String 
        'portNumber':'',                 # Integer
        'simulationMode':'',             # Integer
        'deviceId':'',                   # Integer
        'mpeOptions':'',                 #Integer
        '{ return(0); }':'',
        
    }),
    'IsInitialized':('MPE_isINITIALIZE', {
        'ipAddress':'',                  # String 
        'isInitialized':'',             # (string); 
        '{return(0); }':'',             # (string); 
    
    }),
    'ConnectUsingCOM':('MPE_CONNECTCOM', {
        'comPort':'', # (integer)
        'baudRate':'', # (string); 
        'simulationMode':'',
        'deviceId':'', # (integer)
        ' mpeOptions':'', # (integer)
        '{ return(0); } ':'', # (integer)

    }),
    'IsConnected':('MPE_ISconnected', {
        'deviceId':'', # (integer)
        'isConnected':'', # (string); 
        '{return(0);}':'', # (integer)

    }),
    'Disconnect':('MPE_disconnect', {
        'deviceId':'', # (integer)
        '{ return(0); }':'', # (string);
        
    'Initialize':('MPE_initialize', {
        'deviceId':'', # (integer)
        '{return(0); }':'', # (integer)

    }),
    'ClampFilterPlate':('ClampFilterPlate', {
        'deviceId':'', # (integer)
        '{ return(0); } ':'', # (integer)

    }),
    'CollectionPlatePlaced':('CollectionPlatePlaced', {
        'deviceId':'', # (integer)
        'collectionPlateHeight':'', # (string); 
        'offsetFromNozzles':'', # (string); 
        '{ return(0); } ':'', # (integer;
        
    }),
    'CollectionPlateRemoved':('CollectionPlateRemoved', {
      'deviceId':'', # (integer)
      '{ return(0); } ':'', # (integer;
      
  
    }),
    'FilterPlatePlaced':('MPE_filterplaced', {
        'deviceId':'', # (integer)
        'filterHeight':'', # (string); 
        'nozzleHeight':'', # (string); 
        '{ return(0); } ':'', # (integer;
        
    }),
    'FilterPlateRemoved':('MPE_filterremoved', {
        'deviceId':'', # (integer)
        '{ return(0); } ':'', # (integer;
        
    }),
    'ProcessFilterToCollectionPlate':('MPE_filtertoplate', {
        'deviceId':'', # (integer)
        'controlPoints':'', # (string); 
        'returnPlateToIntegrationArea':'', # (string); 
        '{ return(0); } ':'', # (integer;
        
    }),
    'ProcessFilterToWasteContainer':('MPE_filtertowaste', {
        'deviceId':'', # (integer)
        'controlPoints':'', # (string); 
        'returnPlateToIntegrationArea':'', # (string); 
        'wasteContainerId':'', # (string); 
        'disableVacuumCheck':'', # (string); 
        '{ return(0); } ':'', # (integer;
        
    }),
    'RetrieveFilterPlate':('MPE_getfilterplate', {
        'deviceId':'', # (integer)
        '{ return(0); } ':'', # (integer;       
        
    }),
    'StartMPEVacuum':('MPE_startvaccum', {
        'deviceId':'', # (integer)
        'wasteContainerId':'', # (string); 
        'disableVacuumCheck':'', # (string); 
        '{ return(0); } ':'', # (integer;
    
    }),
    'StartVacuum':('MPE_startvaccumprocess', {
        'deviceId':'', # (integer)
        'wasteContainerId':'', # (string); 
        'seconds':'', # (float); 
        'disableVacuumCheck':'', # (string); 
        '{ return(0); } ':'', # (integer;
    
    }),
    'StopVacuum':('MPE_stopvacuum', {
        'deviceId':'', # (integer)
        '{ return(0); } ':'', # (integer;
        
       
    }),
    'GetVacuumStatus':('MPE_getvacuumstatus', {
        'deviceId':'', # (integer)
        'vacuumActive':'', # (string); 
        '{ return(0); } ':'', # (integer;
        
    }),
    'GetLastError':('MPE_getlasterror', {
        'deviceId':'', # (integer)
        'clearError':'', # (string); 
        'errorMessage':'', # (string); 
        '{ return(0); } ':'', # (integer;

     }),
     'Dispense':('MPE_dispense', {
         'deviceId':'', # (integer)
         'sourceId':'', # (integer); 
         'wellVolume':'', # (float); 
         'flowRate':'', # (float); 
         'needleOffset':'', # (integer;
         '{ return(0); } ':'', # (integer;

    }),
    'DispenseNonStandard':('MPE_dispenseNonS', {
        'deviceId':'', # (integer)
        'sourceId':'', # (string); 
        'wellVolume':'', # (float); 
        'flowRate':'', # (float); 
        'needleOffset':'', # (integer;
        'edgeToWellOffset':'', # (string); 
        'wellToWellOffsets':'[]', # (float); 
        '{ return(0); } ':'', # (integer;
          
     }),
     'Prime':('MPE_prime', {
         'deviceId':'', # (integer)
         'sourceId':'', # (integer); 
         'wellVolume':'', # (float); 
         'flowRate':'', # (float); 
         'wasteContainerId':'', # (integer;
         '{ return(0); } ':'', # (integer;
         
    }),
    'Flush':('MPE_flush', {
        'deviceId':'', # (integer)
        'sourceId':'', # (integer); 
        'wellVolume':'', # (float); 
        'flowRate':'', # (float); 
        'wasteContainerId':'', # (integer;
        '{ return(0); } ':'', # (integer;
        
    }),
    'Evaporate':('MPE_Evaporate', {
        'deviceId':'', # (integer)
        'plateHeight':'', # (integer); 
        'needleOffset':'', # (float); 
        'wellDepth':'', # (float); 
        'evaporateTime':'', # (integer;
        '{ return(0); } ':'', # (integer;
        
     }),
     'EvaporateWithRate':('MPE_EvaporateWrate', {
         'deviceId':'', # (integer)
         'plateHeight':'', # (integer); 
         'needleOffset':'', # (float); 
         'evaporatorTravelDistance':'', # (float); 
         'evaporateTime':'', # (integer;
         'followRate)':'', # (integer;
         '{ return(0); } ':'', # (integer;
         
     }),
     'EvaporatePrepare':('MPE_Evaporateprepare', {
         'deviceId':'', # (integer)
         'temperature':'', # (integer); 
         'pressure':'', # (float); 
         'evaporatorTravelDistance':'', # (float); 
         'timeout)':'', # (integer;
         '{ return(0); } ':'', # (integer;
    
    }),
    'EvaporateEnd':('MPE_EvaporateEND', {
        'deviceId':'', # (integer)
        'timeout)':'', # (integer;
        '{ return(0); } ':'', # (integer;
        
        
    }),
     'GetTemperatureRange':('MPE_temperatureR', {
         'deviceId':'', # (integer)
         'minimumTemperature':'', # (integer;
         'maximumTemperature':'', # (integer;
         '{ return(0); } ':'', # (integer;
         
     }),
      'GetCurrentHeaterStatus':('MPE_getheaterstat', {
          'deviceId':'', # (integer)
          'reset':'', # (integer;
          'currentEvaporatorTemperature':'', # (integer;
          'currentGasTemperature':'', # (integer;
          'heating':'', # (integer;
          '{ return(0); } ':'', # (integer;
          
     }),
      'GetHeaterTemperatureRange':('MPE_getheatersTR', {
          'deviceId':'', # (integer)
          'reset':'', # (integer;
          'minimumEvaporatorTemperature':'', # (integer;
          'maximumEvaporatorTemperature':'', # (integer;
          'minimumGasTemperature':'', # (integer;
          'maximumGasTemperature':'', # (integer;
          'targetTemperature':'', # (integer;
          'heating':'', # (integer;
          '{ return(0); } ':'', # (integer;
    
     }),
      'SetSourceConfiguration':('MPE_sourceconfig', {
          'deviceId':'', # (integer)
          '{ return(0); } ':'', # (integer;
     
    }),
     'GetSourceConfiguration':('MPE_getsourceconfig', {
         'deviceId':'', # (integer)
         '{ return(0); } ':'', # (integer;
     
    }),
     'ClearSourceConfiguration':('MPE_clearsourceconfig', {
          'deviceId':'', # (integer)
          'reset':'', # (integer;
          '{ return(0); } ':'', # (integer;
         
     }),
      'StartContainerCalibration':('MPE_calibrationSTART', {
          'deviceId':'', # (integer)
          'sourceId':'', # (integer;
          'volume':'', # (integer;
          '{ return(0); } ':'', # (integer;
   
    }),
     'CancelContainerCalibration':('MPE_calibrationCANCEL', {
         'deviceId':'', # (integer)
         'sourceId':'', # (integer;
         '{ return(0); } ':'', # (integer;
    
    }),
     'GetContainerCalibration':('MPE_calibrationGET', {
         'deviceId':'', # (integer)
         'sourceId':'', # (integer;
         'emptyReading':'', # (integer;
         'fullReading':'', # (integer;
         'calibrationDate':'', # (integer;
         '{ return(0); } ':'', # (integer;
     }),
      'MeasureEmptyContainer':('MPE_calibrationMEASURE', {
          'deviceId':'', # (integer)
          'sourceId':'', # (integer;
          '{ return(0); } ':'', # (integer;
