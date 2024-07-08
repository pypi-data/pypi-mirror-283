from pyspark.sql.functions import *
from itertools import chain
from pyspark.sql.window import Window


class encoding_SM:
  def __init__(self, df):
    self.df = df.orderBy('InfusionID', 'StartTime')
    self.window_spec = Window.orderBy(col('InfusionID'), col('StartTime'))
    self.encode_df = self.encode()

  def encoding_single(self):
    # creating the dictionary of encodings
    encoding = {'Module Status Changed' : 2, 'Infusion Reprogrammed': -1,
                'Infusion Stopped': 1, 'Infusion Alarmed': 1,
                'Same Drug': -1, 'Infusion Paused': 1,
                'Weight Change': -1, 'Infusion Alerted': -1,
                'Drug Cancel': -1, 'Stop Secondary': -1,
                'Infusion Started': 0, 'Infusion Alert Resolved': -1,
                'Partial Dose': -1, 'Infusion Transitioned': 2
                }
    # creating the dictionary map
    encoding_map = create_map([lit(i) for i in chain(*encoding.items())])


    infusion = self.df.select(col('_PT'), col('InfusionID'),
              col('PCUSerialNumber'), col('ModuleSerialNumber'),
              col('DrugName'),
              col('InfusionProgramming'), col('StartTime'), col('StartReasonCode'),
              col('ActualDurationSeconds'), col('Alarm'), col('State'),
              col('InfusionType'), col('InfusionSetup'),
              col('Rate'), col('RateUnit'), col('ProgrammedDose')
              ).orderBy(
                  col('InfusionID'),
                  col('StartTime')
                  ).withColumn('EncodedStartReason',
                                encoding_map[col('StartReasonCode')]).select(col('_PT'), col('InfusionID'),
              col('PCUSerialNumber'), col('ModuleSerialNumber'),
              col('DrugName'),
              col('InfusionProgramming'), col('StartTime'), col('StartReasonCode'), col('EncodedStartReason'),
              col('ActualDurationSeconds'), col('Alarm'), col('State'),
              col('InfusionType'), col('InfusionSetup'),
              col('Rate'), col('RateUnit'), col('ProgrammedDose'))

    return infusion

  def encoding_multiple(self):
    def encoding_multi(df_spark, strt_reason: str, window_sp = self.window_spec):
      # create columns containing information from sliding window
      df_spark = (
          df_spark.withColumn('EncodedStartReason_prev', lag('EncodedStartReason', 1).over(window_sp))
                  .withColumn('EncodedStartReason_next', lead('EncodedStartReason', 1).over(window_sp))
      )

      df_spark = df_spark.withColumn(
          'EncodedStartReason', when( # instance for code: continuous
              (col('StartReasonCode') == strt_reason) &
              (col('EncodedStartReason_prev')== 0) &
                (col('EncodedStartReason_next').isin(-1, 1)), 2)
          .when( # instance for code: stop
              (col('StartReasonCode') == strt_reason) &
              ((col('EncodedStartReason_prev')== 0) | (col('EncodedStartReason_prev').isNull()))  &
              (col('EncodedStartReason_next').isin(-1, 1, 2) == False), 1
          ).when( # instace for code: start
              (col('StartReasonCode') == strt_reason) &
                  (col('EncodedStartReason_prev') != 0) &
                  (col('EncodedStartReason_next').isin(-1, 1)),
                  0).otherwise(col('EncodedStartReason'))
      )

      return df_spark


    df_encoded = self.encoding_single()

    multi = ['Infusion Delayed', 'Infusion Completed',
              'Infusion NEOI Started', 'Infusion Restarted',
              'Max Limit Reached', 'Infusion KVO Started']

    for k in range(len(multi)):
      for i_code in multi:
        df_encoded = encoding_multi(df_encoded, i_code)

    return df_encoded

  def encode(self):
    df_enc = self.encoding_multiple()

    state_encoding = {'Infusion Completed in KVO': 2,
                      'Infusion Delayed': 1, 'Infusion Idle': 1,
                      'Infusion Paused': 1, 'Non-Infusion Other': 1,
                      'Infusion Completed' : 1, 'Infusion Alarm': 1}
    # creating the dictionary map
    encoding_map_ = create_map([lit(i) for i in chain(*state_encoding.items())])

    df_enc = df_enc.withColumn(
        'EncodedStartReason', when(
            col('State').isin(*state_encoding.keys()), encoding_map_[col('State')]
        ).when(
            (col('EncodedStartReason').isNull()) & (col('State') == 'Infusing'), 2
            ).otherwise(col('EncodedStartReason'))
    ).drop('EncodedStartReason_prev', 'EncodedStartReason_next')

    return df_enc

class infusion_desc(encoding_SM):
  def __init__(self, df):
    # initialize parameters of parent class
    super().__init__(df)
    # obtain the list of unique infusion ids
    self.infusion_id = [i['InfusionID'] for i in self.encode_df.select('InfusionID').distinct().collect()]

  def row_detail(self):
    # obtain value of previous encoding
    data = self.encode_df.withColumn('EncodedStartReason_prev', lag('EncodedStartReason', 1).over(self.window_spec))

    # obtain the row number of each record to serve as index
    data = data.withColumn('row_number', row_number().over(self.window_spec))

    return data

  def inf_sum_encode(self):
    data_sum = self.row_detail()
    infusion_codes = self.infusion_id
    window_partition = self.window_spec.partitionBy('InfusionID')

    # obtain the minimum row number for each InfusionID
    data_sum = data_sum.withColumn('min_row_number', min('row_number').over(window_partition))

    # replace min row number with None
    data_sum = data_sum.withColumn('EncodedStartReason_prev',
                                   when((col('row_number') == col('min_row_number')),
                                        lit(None)).otherwise(col('EncodedStartReason_prev')))

    # drop the row_number and min_row_number
    data_sum = data_sum.drop('row_number', 'min_row_number')

    return data_sum

  def infusion_time(self):
    def infusion_length(df_data = self.inf_sum_encode()):
      # obtain the length of each infusion time in seconds
      df_data = df_data.withColumn(
          'StartTime_prev', lag('StartTime', 1).over(self.window_spec)
      )

      # carry out the substraction:
      df_data = df_data.withColumn(
          'infusion_time', when(
              (col('EncodedStartReason_prev').isin([0, 2])) &
              (col('EncodedStartReason').isin([-1,0,1,2])),
                (unix_timestamp(col('StartTime')) - unix_timestamp(col('StartTime_prev')))
              ).otherwise(lit(0))
      )

      return df_data

    infusion_info = infusion_length()

    # aggregate the data to find the summary of each infusionid
    infusion_info = infusion_info.groupBy('InfusionID',
                                          'PCUSerialNumber',
                                          'ModuleSerialNumber',
                                          ).agg(
                                              sum('infusion_time').alias('InfusionTime'),
                                              min('StartTime').alias('BOP_StartTime'),
                                              max('StartTime').alias('EOP_StartTime')
                                              ).withColumn(
                                                  'EqActiveTime', (unix_timestamp(col('EOP_StartTime')) - unix_timestamp(col('BOP_StartTime')))
                                              ).select(
                                                  to_date(col('BOP_StartTime')).alias('BOP_StartTime'),
                                                  to_date(col('EOP_StartTime')).alias('EOP_StartTime'),
                                                  col('InfusionID'), col('PCUSerialNumber'),
                                                  col('ModuleSerialNumber'), col('InfusionTime'), col('EqActiveTime')
                                              )

    return infusion_info