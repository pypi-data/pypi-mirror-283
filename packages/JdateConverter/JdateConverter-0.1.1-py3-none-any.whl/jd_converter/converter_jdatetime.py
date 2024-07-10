
class JDateTimeConverter:
    '''
    this class convert to or from jalali datetime 
    
    obj1=JDateTimeConverter
    obj1.previous_days_to_datetime(5,type_kind='str',str_returns_format='%Y/%m/%d')
    '''


    @staticmethod
    def previous_days_to_datetime(previus_day=1,
                                  date_format='jalali',
                                  type_kind='str',
                                  str_returns_format="%Y%m%d",
                                  ): 
        # import  jdatetime 
        from datetime import datetime
        
        '''
        this function gets an integer and returns it to string format that we specify 
        :param previus_day:int like 5 | 7 which we want to returns the data ,for  e.g if we are 2024/05/07 and if we consider 3    it  returns  2024/05/04 
        :param date_format: jalali | gregorian 
        :param returns_format: like %Y%m%d or %Y%m%d or...
        :param type_kind: str | datetime 
        
        returns previous_days_to_datetime(5,type_kind='str',str_returns_format='%Y/%m/%d')
        '1403/04/14'
        ''' 
        if date_format =='jalali':
            from jdatetime import timedelta ,datetime
            days_previous=timedelta(days=previus_day)
            today=datetime.now()
        elif date_format =='gregorian': 
            from datetime import datetime ,timedelta
            today=datetime.now()
            days_previous=timedelta(days=previus_day)
        day_formated=today-days_previous
        return day_formated.strftime(format=str_returns_format) if type_kind =='str' else day_formated



    @staticmethod
    def previous_hours_to_datetime(hours_ago=None,
                                   date_format = 'gregorian'
                                   ):
    
        '''
        the function returns n hours ago to json format 
        params :hours_ago  > if None it retuens just now and if gets the numbers e.g 3 returns 3 hours ago
        :param date_format:  = 'gregorian'
        returns : datetime str  | datetime str 
                '2024-06-24 10-16-12'
        '''
        
        if date_format =='gregorian':  
            from datetime import datetime ,timedelta
        elif date_format =='jalali':  
            from jdatetime import datetime ,timedelta
        if hours_ago:
            date_time = datetime.now() - timedelta(hours=hours_ago)
        elif hours_ago is None or hours_ago == 0:
            date_time = datetime.now()
        return (date_time.strftime("%Y-%m-%d %H:%M:%S"))

    @staticmethod
    def jalali_converter(input_month=None):
        '''
        :param input_month:if it gets digits like 2 it returns relevent month like اردیبهشت . 
                            and if it gets farsi strings like دی it returns relevent digit like 10 
        :return: e.g  
        jalli_converter('مرداد')  > 5
        jalli_converter(7) > 'مهر'
        
        '''
        mah_be_borg={
            'فروردین': 1 ,
            'اردیبهشت':2 ,
            'خرداد':3 ,
            'تیر': 4,
            'مرداد': 5,
            'شهریور':6 ,
            'مهر': 7,
            'آبان':8 ,
            'آذر': 9,
            'دی': 10,
            'بهمن':11 ,
            'اسفند':12 ,
        }

        borg_be_mah={ val:key for key , val in mah_be_borg.items()}
        if isinstance(input_month,str):
            return mah_be_borg[input_month]
        elif isinstance(input_month,int):
            return borg_be_mah[input_month]



