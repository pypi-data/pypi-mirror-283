from logger_log import log_message
import pytz
from datetime import datetime
class dataOperations:
    def __init__(self, db_connection  = None, predict_args = []) -> None:
        self.conn = db_connection
        self.predict_args = predict_args
        self.db_timezone = predict_args['db_timezone']
        self.app_timezone = predict_args['app_timezone']
        self.tz = pytz.timezone(self.app_timezone)

    def get_max_training_date(self,table_name): 
        max_date = datetime.now(self.tz)
        try:
            sql = f"""
                select max(data_updated_at at time zone '{self.db_timezone}') as max_date from {table_name} 
            """
            result = self.conn.execute_select_query(sql)
            if len(result)>0:
                max_date = result[0]['max_date']
            return max_date
        except Exception as ex:
            log_message('error',f"Errors getting max_date from {table_name}.  Details : {str(ex)}")
            return max_date

    def append_feedback_data_for_training(self,model_type, max_data_date):
        try:
            if model_type=='voice':
                sql = f"""
                    INSERT INTO app.call_predictions_training
                        select 
                            case when (call_duration_xx_percent::float)>{self.predict_args['duration_percent']} then 1 else 0 end as duration_rate,
                            case when call_rate_per_hour::int4>{self.predict_args['call_rate']} then 1 else 0 end as call_rate,
                            case when unknown_percent::float > {self.predict_args['unknown_percent']} then 1 else 0 end as unk_rate, 
                            case when unallocated_percent::float > {self.predict_args['unallocated_percent']} then 1 else 0 end as unalloc_rate,
                            case when left(scam_status,4)='SCAM' then 'SCAM' else 'NOSCAM' end as scam_status,
                            'Feedback' as data_type,
                            current_timestamp as data_updated_at
                        from app.call_predictions cp 
                            where 
                                feedback_flag ='Y'
                                and (feedback_flag_date_time at time zone '{self.predict_args['db_timezone']}')>'{max_data_date}'::timestamptz
                """   
            else:
                sql = f"""
                    insert into app.sms_predictions_training
                        select 
                            case when msg_ratio_percent>{self.predict_args['msg_ratio_percent_value']} then 1 else 0 end as msg_ratio_percent,
                            case when msg_ratio<{self.predict_args['msg_ratio_value']} then 1 else 0 end as msg_ratio, 
                            url_ind, 
                            reward_ind, 
                            opt_out_ind, 
                            email_ind, 
                            phone_ind,
                            url_ind_1, 
                            case when left(scam_status,4)='SCAM' then 'SCAM' else 'NOSCAM' end as scam_status,
                            'Feedback' as data_type,
                            current_timestamp as data_updated_at
                        from app.sms_predictions sp 
                            where 
                                feedback_flag ='Y'
                                and (feedback_flag_date_time at time zone '{self.predict_args['db_timezone']}')>'{max_data_date}'::timestamptz
                """                     
            result = self.conn.execute_insert_query(sql)
            self.conn.conn.commit()
            return True
        except Exception as ex:
            log_message('error',f"Unable to insert training data! Details : {str(ex)}")
            return False
        
    def get_training_data (self, model_type):
        result = []
        try:
            if model_type=='voice':
                sql = f"""select 
                        duration_rate,
                        call_rate,
                        unk_rate, 
                        unalloc_rate, 
                        class_type
                    from app.call_predictions_training"""
            else:
                sql = f"""select 
                        msg_ratio_percent,
                        msg_ratio,
                        url_ind, 
                        reward_ind, 
                        opt_out_ind, 
                        email_ind, 
                        phone_ind,
                        url_ind_1, 
                        class_type
                    from app.sms_predictions_training"""
            result = self.conn.execute_select_query(sql)
            return result
        except Exception as ex:
            log_message('error',f"Unable to get training data for model_type={model_type}")
            return result

    def get_model_details(self, model_type):
        ret_val = {
            "key" : "",
            "mj_version" : 0,
            "version" : 0
        }
        sql = f"""select * from meta.ml_model_versions where model_type='{model_type}' order by id DESC limit 1"""
        result = self.conn.execute_select_query(sql)
        if len(result)>0:
            ret_val["key"] = result[0]['model_file_location']
            ret_val["mj_version"] = result[0]['model_ver_major']
            ret_val["version"] = result[0]['model_ver_minor']
        return ret_val
    
    def get_model_file_name(self,model_type):
        file_name = ""
        mj_version = 0
        version = 1
        try:
            sql = f"select max(model_ver_major) as mj_version,max(model_ver_minor)+1 as version from meta.ml_model_versions where model_type = '{model_type}'"
            result = self.conn.execute_select_query(sql)
            if len(result)>0:
                mj_version=result[0]['mj_version']
                version = result[0]['version']
                file_name = f"""scam_call_prediction_model_{str(datetime.now(self.tz)).replace(".","_")}_{str(mj_version).replace(".","_")}_{str(version).replace(".","_")}.pkl""".replace(" ","_")
            return file_name, mj_version, version
        except Exception as ex:
            log_message('error',f"Errors while collecting model version for {model_type}. Details : {str(ex)}")
            return file_name, mj_version, version

    def update_model_version(self, model_type,file_name, key, mj_version, version):
        try:
            sql = f"""insert into meta.ml_model_versions 
                    (model_type, model_file_name, model_file_location, model_ver_major,model_ver_minor)
                    values (
                        '{model_type}', '{file_name}', '{key}',{mj_version},{version}
                    ) 
                """
            self.conn.execute_void_query(sql)
            self.conn.conn.commit()
            return True
        except Exception as ex:
            log_message('error',f"Unable to update model version! Errors : {str(ex)}")
            return False

    def get_run_id(self, model_type):
        ret_value = 0
        #scam_call_prediction - scam_sms_prediction
        isql = f"select run_id+1 as run_id from app.run_ids where run_type='{model_type}'"
        temp = self.conn.execute_select_query(isql)
        if temp[0]["run_id"] is None:
            ret_value = 1
        else:
            ret_value =  temp[0]["run_id"]
        return ret_value
        
    def update_run_id(self, run_id, model_type):
        ret_value = False
        #client.begin_transaction('call_prediction_update_run_id')
        isql = f"""update app.run_ids set run_id = {run_id} where run_type='{model_type}'""" 
        if not self.conn.execute_void_query(isql):
            log_message('error',
                f"Unable to update Run_id to Master table. Please try again."
            )
            ret_value= False
        else:
            ret_value= True
        return ret_value

    def build_aggregate_sql(self, model_type):
        filter_customer = True if self.predict_args['filter_customer'].lower()=='true' else False
        customer_filter =  self.predict_args['customer_filter']
        log_message('info',f"filter-customer? = {filter_customer}, and customer filter is : {customer_filter}")
        if model_type=='voice':
            sql = f"""
                select 
                    mvp,
                    min(cust_id) as cust_id,
                    min(cust_name) as cust_name,
                    min(cust_account_id) as cust_account_id,
                    min(subscription_id) as subscription_id,
                    trans_calling_number,
                    min(call_direction) as call_direction,
                    other_actor_id as actor_id,
                    min(start_datetime at time zone '{self.predict_args['db_timezone']}') as min_start_date_time,
                    max(start_datetime at time zone '{self.predict_args['db_timezone']}') as max_start_date_time,
                    min(allocated_cust_id) as allocated_cust_id,
                    min(allocated_cust_name) as allocated_cust_name,
                    min(allocated_cust_account_id) as allocated_cust_account_id,
                    min(allocated_subscription_id) as allocated_subscription_id,
                    min(calling_carrier) as calling_carrier,
                    count(*) as total_count,
                    avg(call_duration) as avg_call_duration,
                    cast(max(date_part('HOUR',start_datetime  at time zone '{self.predict_args['db_timezone']}'))-min(date_part('HOUR',start_datetime  at time zone '{self.predict_args['db_timezone']}')) + 1 as integer) as total_hours,
                    ROUND(cast(count(*)/ (max(date_part('HOUR',start_datetime at time zone '{self.predict_args['db_timezone']}'))-min(date_part('HOUR',start_datetime at time zone '{self.predict_args['db_timezone']}')) + 1) as numeric),2) as call_rate_count,
                    sum(case when call_duration<={self.predict_args["duration"]} then 1 else 0 end) as duration_count,
                    round(sum(case when call_duration<={self.predict_args["duration"]} then 1 else 0 end)/cast(count(*) as numeric),2) as duration_percent,
                    sum(case when calling_number_presentation_option_value='UNKNOWN' then 1 else 0 end) as unk_count,
                    round(sum(case when calling_number_presentation_option_value='UNKNOWN' then 1 else 0 end)/cast(count(*) as numeric),2) as unk_per,
                    sum(case when release_cause_value='UNALLOCATED_NUMBER' then 1 else 0 end) as unallocated_count,
                    round(sum(case when release_cause_value='UNALLOCATED_NUMBER' then 1 else 0 end)/cast(count(*) as numeric),2) as unallocated_per,
                    case when round(sum(case when call_duration<={self.predict_args["duration"]} then 1 else 0 end)/cast(count(*) as numeric),2)>{self.predict_args['duration_percent']} then 1 else 0 end as duration_rate,
                    case when round(sum(case when calling_number_presentation_option_value='UNKNOWN' then 1 else 0 end)/cast(count(*) as numeric),2)>{self.predict_args['unknown_percent']} then 1 else 0 end as unk_rate,
                    case when round(sum(case when release_cause_value='UNALLOCATED_NUMBER' then 1 else 0 end)/cast(count(*) as numeric),2)>{self.predict_args['unallocated_percent']} then 1 else 0 end as unalloc_rate,
                    case when ROUND(cast(count(*)/ (max(date_part('HOUR',start_datetime at time zone '{self.predict_args['db_timezone']}'))-min(date_part('HOUR',start_datetime at time zone '{self.predict_args['db_timezone']}')) + 1) as numeric),2)>{self.predict_args["call_rate"]} then 1 else 0 end  as call_rate,
                    min((CURRENT_TIMESTAMP at time zone '{self.predict_args['db_timezone']}')::date)::text as group_id
                from app.cdrs cdr 
                    where lower(call_direction::text)<>'inbound' 
                    and not exists (select id from app.call_prediction_details cpd where cpd.id=cdr.id) 
                """
            if not self.predict_args["unknown_customer"]:
                sql = (
                    sql
                    + f""" and (cust_account_id <> 'UNKNOWN' and allocated_cust_account_id <> 'UNKNOWN')"""
                )
            isql = ""
            if filter_customer:
                if len(customer_filter)>0:
                    filters = customer_filter.split("||")
                    for filter in filters:
                        ip_filter = "false"
                        ip_address = ""
                        atts = filter.split(",")
                        if len(atts)>0:
                            mvp = atts[0].split(":")[1]
                            actorid=atts[1].split(":")[1]     
                            if len(atts)>2:                   
                                ip_filter = atts[2].split(":")[1] 
                                ip_address = atts[3].split(":")[1]
                            isql = isql + f" ( mvp = '{mvp}' and other_actor_id = {actorid}  "
                            if ip_filter=="true":
                                if len (ip_address)>0:
                                    isql = isql + f" and ip_address ='{ip_address}' "
                            isql = isql + " ) or"
                if len(isql)>0:
                    isql = isql[:-2]
                    sql = sql + f" and ({isql}) "
            #new code ends here.
            sql = (
                sql
                + f""" group by mvp, actor_id, trans_calling_number having count(*)>{self.predict_args["count"]}"""
            )

            if self.predict_args["use_call_rate"]:
                sql = (
                    sql
                    + f""" and ROUND(cast(count(*)/ (max(date_part('HOUR',start_datetime at time zone '{self.predict_args['db_timezone']}'))-min(date_part('HOUR',start_datetime at time zone '{self.predict_args['db_timezone']}')) + 1) as numeric),2)>{self.predict_args["call_rate"]}"""
                )

            if self.predict_args["use_unknown_percent"]:
                sql = (
                    sql
                    + f""" and round(sum(case when calling_number_presentation_option_value='UNKNOWN' then 1 else 0 end)/cast(count(*) as numeric),2)>{self.predict_args["unknown_percent"]}"""
                )

            if self.predict_args["use_duration_percent"]:
                sql = (
                    sql
                    + f""" and round(sum(case when call_duration<={self.predict_args["duration"]} then 1 else 0 end)/cast(count(*) as numeric),2) >= {self.predict_args["duration_percent"]}"""
                )

            if self.predict_args["use_unallocated_percent"]:
                sql = (
                    sql
                    + f""" and round(sum(case when release_cause_value='UNALLOCATED_NUMBER' then 1 else 0 end)/cast(count(*) as numeric),2) >= {self.predict_args["unallocated_percent"]}"""
                )  
        else:
            sql = f"""
                select 
                    a.mvp as mvp,
                    a.cust_id,
                    a.cust_name,
                    a.cust_account_id,	
                    a.subscription_id,
                    a.predicted_cli,
                    a.call_direction,
                    a.actor_id as actor_id,
                    a.min_start_date_time,
                    a.max_start_date_time,
                    a.calling_carrier,
                    a.sdr_count,
                    b.content_decrypted,
                    a.alpha_ind,
                    b.url_ind,
                    b.url_ind_1,
                    b.reward_ind,
                    b.opt_out_ind,
                    b.word_count,
                    b.ignore_ind,
                    b.this_msg_count,
                    case when round(b.this_msg_count / a.sdr_count::decimal * 100,2)>{self.predict_args['msg_ratio_percent_value']} and round(a.unique_msg_count / a.sdr_count::decimal * 100,2)<{self.predict_args['msg_ratio_value']} then 1 else 0 end as msg_ratio_ind,
                    round(a.unique_msg_count / a.sdr_count::decimal * 100,2) as msg_ratio,
                    round(b.this_msg_count / a.sdr_count::decimal * 100,2) as msg_ratio_percent,
                    0 as email_ind,
                    0 as phone_ind,
                    a.sdr_count as total_msg_count,
                    a.to_number_count,
                    a.unique_msg_count,
                    case when round(a.unique_msg_count / a.sdr_count::decimal * 100,2)<{self.predict_args['msg_ratio_value']} then 1 else 0 end as msg_ratio_flag,
                    case when round(b.this_msg_count / a.sdr_count::decimal * 100,2)>{self.predict_args['msg_ratio_percent_value']} then 1 else 0 end as msg_ratio_percent_flag,
                    (a.min_start_date_time::date)::text as group_id
                from 
                    (
                        select 
                            mvp,
                            actor_id,
                            predicted_cli,
                            count(distinct content_decrypted) as unique_msg_count,
                            count(distinct to_number) as to_number_count, 
                            count(*) as sdr_count,
                            min(calling_carrier) as calling_carrier,
                            min(cust_id) as cust_id,
                            min(cust_name) as cust_name,
                            min(cust_account_id) as cust_account_id,
                            min(direction) as call_direction,
                            min(subscription_id) as subscription_id ,
                            min(sent_time at time zone '{self.predict_args['db_timezone']}') as min_start_date_time,
                            max(sent_time at time zone '{self.predict_args['db_timezone']}') as max_start_date_time,
                            CASE
                                WHEN predicted_cli::text ~* '[a-zA-Z+ !@#$%^&*]'::text THEN 1
                                ELSE 0
                            END AS alpha_ind 
                        from app.temp_results
                            group by 
                                mvp,
                                actor_id,
                                predicted_cli 
                                having count(distinct to_number )>1
                    ) a, 
                    (
                        select 
                            mvp,
                            actor_id,
                            predicted_cli,
                            content_decrypted,
                            0 as url_ind,
                            0 as url_ind_1,
                            0 as reward_ind,
                            0 as opt_out_ind,
                            0 as word_count,
                            0 as ignore_ind,
                            count(*) as this_msg_count
                        from app.temp_results
                            group by 
                                mvp,
                                actor_id,
                                predicted_cli,
                                content_decrypted
                    ) b 
                    where  
                        a.mvp = b.mvp 
                        and a.actor_id = b.actor_id 
                        and a.predicted_cli=b.predicted_cli
                        and round(b.this_msg_count / a.sdr_count::decimal * 100,2)>1
            """
            if not self.predict_args["unknown_customer"]:
                sql = (
                    sql
                    + f""" and (cust_account_id <> 'UNKNOWN') """
                )
            isql = ""
            if filter_customer:
                if len(customer_filter)>0:
                    filters = customer_filter.split("||")
                    for filter in filters:
                        ip_filter = "false"
                        ip_address = ""
                        atts = filter.split(",")
                        if len(atts)>0:
                            mvp = atts[0].split(":")[1]
                            actorid=atts[1].split(":")[1]     
                            if len(atts)>2:                   
                                ip_filter = atts[2].split(":")[1] 
                                ip_address = atts[3].split(":")[1]
                            isql = isql + f" ( a.mvp = '{mvp}' and a.actor_id = {actorid}  "
                            """
                            if ip_filter=="true":
                                if len (ip_address)>0:
                                    isql = isql + f" and ip_address ='{ip_address}' "
                            """
                            isql = isql + " ) or"

                if len(isql)>0:
                    isql = isql[:-2]
                    sql = sql + f" and ({isql}) "

            #new code ends here.  
        return sql

    def execute_aggregate_query(self, model_type):
        result = []
        try:
            sql = self.build_aggregate_sql(model_type)
            result = self.conn.execute_select_query(sql)
            return result
        except Exception as ex:
            log_message('error',f"Unable to execute aggregate query. Error : {str(ex)}")
            return result

    def get_data_for_decryption(self):
        try:
            results = []
            sql = """
                select
                    mvp,
                    cust_id,
                    actor_name as cust_name,
                    cust_account_id,
                    subscription_id,
                    from_number AS predicted_cli,
                    to_number,
                    direction,
                    actor_id,
                    sent_time,
                    calling_carrier,
                    content,
                    '' as content_decrypted
                FROM app.sdrs sdr
                    WHERE 1 = 1 AND lower(direction::text) <> 'inbound'::text 
                        AND from_number::text <> to_number::text
                        and not exists (select id from app.sms_prediction_details spd where spd.id=sdr.id)
            """
            results = self.conn.execute_select_query(sql)
            return results
        except Exception as ex:
            log_message('error',f"Unable to get data for decription! Error: {str(ex)}")
            return results

    def truncate_staging_data(self):
        try:
            sql = "truncate table app.temp_results"
            result = self.conn.execute_void_query(sql)
            return True
        except Exception as ex:
            log_message('error',f"Unable to truncate staging data! Error : {str(ex)}")
            return False
                   
    def insert_staging_data(self, table_name, dataset, columns, convert = False):
        try:
            result = self.conn.execute_using_copy_bulk(table_name,dataset, columns, convert)
            return result
        except Exception as ex:
            log_message('error',f"Unable to insert staging data for prediction. Error : {str(ex)}")
            return False