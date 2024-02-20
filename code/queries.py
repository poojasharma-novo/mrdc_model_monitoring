current_data = (r""" 
with mrdc_score as (
select  mrdc_id, 
-- date(created_at) as created_mrdc, 
TO_NUMBER(COALESCE(json_extract_path_text(output, 'score'), null )) as score,
TO_NUMBER(COALESCE(json_extract_path_text(input,'ach_c_median_past30d' ), null )) as ach_c_median_past30d,
TO_NUMBER(COALESCE(json_extract_path_text(input,'ach_c_std_past30d' ), null )) as ach_c_std_past30d,
TO_NUMBER(COALESCE(json_extract_path_text(input,'ach_d_avg_past10d' ), null )) as ach_d_avg_past10d,
TO_NUMBER(COALESCE(json_extract_path_text(input,'ach_d_median_past30d' ), null )) as ach_d_median_past30d,
TO_NUMBER(COALESCE(json_extract_path_text(input, 'amount' ), null )) as  amount,
TO_NUMBER(COALESCE(json_extract_path_text(input,'avg_running_balance_past30d' ), null )) as avg_running_balance_past30d,
TO_NUMBER(COALESCE(json_extract_path_text(input,'card_txn_std_past10by30d' ), null )) as card_txn_std_past10by30d,
TO_NUMBER(COALESCE(json_extract_path_text(input,'card_txn_std_past10d' ), null )) as card_txn_std_past10d,
TO_NUMBER(COALESCE(json_extract_path_text(input,'credit_txn_avg_past10by30d' ), null )) as credit_txn_avg_past10by30d,
TO_NUMBER(COALESCE(json_extract_path_text(input,'credit_txn_avg_past10d' ), null )) as credit_txn_avg_past10d,
TO_NUMBER(COALESCE(json_extract_path_text(input,'credit_txn_count_past10by30d' ), null )) as credit_txn_count_past10by30d,
TO_NUMBER(COALESCE(json_extract_path_text(input,'credit_txn_std_past30d' ), null )) as credit_txn_std_past30d,
TO_NUMBER(COALESCE(json_extract_path_text(input,'debit_txn_count_past10by30d' ), null )) as debit_txn_count_past10by30d,
TO_NUMBER(COALESCE(json_extract_path_text(input,'ein_ssn' ), null )) as ein_ssn,
TO_NUMBER(COALESCE(json_extract_path_text(input,'is_between1000and5000' ), null )) as is_between1000and5000,
TO_NUMBER(COALESCE(json_extract_path_text(input,'is_between200and1000' ), null )) as is_between200and1000,
TO_NUMBER(COALESCE(json_extract_path_text(input,'mrdc_c_avg_past30d' ), null )) as mrdc_c_avg_past30d,
TO_NUMBER(COALESCE(json_extract_path_text(input,'mrdc_c_median_past10by30d' ), null )) as mrdc_c_median_past10by30d,
TO_NUMBER(COALESCE(json_extract_path_text(input,'od_count_past30d' ), null )) as od_count_past30d,
TO_NUMBER(COALESCE(json_extract_path_text(input,'past10by30d_between200and1000_ratio' ), null )) as past10by30d_between200and1000_ratio,
TO_NUMBER(COALESCE(json_extract_path_text(input,'past10by30d_check_ratio' ), null )) as past10by30d_check_ratio,
TO_NUMBER(COALESCE(json_extract_path_text(input,'past10by30d_returned_check_ratio' ), null )) as past10by30d_returned_check_ratio,
TO_NUMBER(COALESCE(json_extract_path_text(input,'pd_avg_past10d' ), null )) as pd_avg_past10d,
TO_NUMBER(COALESCE(json_extract_path_text(input,'rejected_past10by30d_between200and1000_ratio' ), null )) as rejected_past10by30d_between200and1000_ratio,
TO_NUMBER(COALESCE(json_extract_path_text(input,'returned_past30d_avg_check_amount' ), null )) as returned_past30d_avg_check_amount,
TO_NUMBER(COALESCE(json_extract_path_text(input,'rn_past30d_avg_check_amount' ), null )) as rn_past30d_avg_check_amount,
TO_NUMBER(COALESCE(json_extract_path_text(input,'past10by30d_lessthan200_ratio' ), null )) as past10by30d_lessthan200_ratio
from FIVETRAN_DB.PROD_NOVO_API_PUBLIC.MRDC_RISK_DECISION_SCORES
where type ilike 'novo_ds_risk_score' 
)
, check_status as (
select id, date(created_at) as created_status, status, amount as total_amount from FIVETRAN_DB.PROD_NOVO_API_PUBLIC.REMOTE_DEPOSIT_CHECKS 
where created_status >= date_trunc('month', current_date()) - interval '1 month' 
AND created_status < date_trunc('month', current_date())

)

select a.mrdc_id, b.created_status, b.total_amount, a.score, b.status, a.ach_c_median_past30d, a.ach_c_std_past30d,
a.ach_d_avg_past10d, a.ach_d_median_past30d, a.amount, a.avg_running_balance_past30d, a.card_txn_std_past10by30d, a.card_txn_std_past10d, 
a.credit_txn_avg_past10by30d, a.credit_txn_avg_past10d, a.credit_txn_count_past10by30d, a.credit_txn_std_past30d, a.debit_txn_count_past10by30d, 
a.ein_ssn, a.is_between1000and5000, a.is_between200and1000, a.mrdc_c_avg_past30d, a.mrdc_c_median_past10by30d, a.od_count_past30d, a.past10by30d_between200and1000_ratio,
a.past10by30d_check_ratio, a.past10by30d_returned_check_ratio, a.pd_avg_past10d, a.rejected_past10by30d_between200and1000_ratio, a.returned_past30d_avg_check_amount, 
a.rn_past30d_avg_check_amount, a.past10by30d_lessthan200_ratio
from mrdc_score a inner join check_status b on a.mrdc_id = b.id """)


reference_data = (r""" with mrdc_score as (select * from PROD_DB.ADHOC.MRDC_RISK_SCORING_HISTORICAL ) 

, check_status as (
select id, date(created_at) as created_status, status, amount as total_amount from FIVETRAN_DB.PROD_NOVO_API_PUBLIC.REMOTE_DEPOSIT_CHECKS 
where created_status between date('2022-01-01') and date('2022-12-31') order by created_status 
)

-- select c.*, b.* from mrdc_score c right join check_status b on "mrdc_id"  = id

select a."mrdc_id", b.created_status, b.total_amount, a."predictions", b.status, a."ach_c_median_past30d", a."ach_c_std_past30d",
a."ach_d_avg_past10d", a."ach_d_median_past30d", a."amount", a."avg_running_balance_past30d", a."card_txn_std_past10by30d", a."card_txn_std_past10d",
a."credit_txn_avg_past10by30d", a."credit_txn_avg_past10d", a."credit_txn_count_past10by30d", a."credit_txn_std_past30d", a."debit_txn_count_past10by30d", 
a."ein_ssn", a."is_between1000and5000", a."is_between200and1000", a."mrdc_c_avg_past30d", a."mrdc_c_median_past10by30d", a."od_count_past30d", 
a."past10by30d_between200and1000_ratio", a."past10by30d_check_ratio", a."past10by30d_returned_check_ratio", a."pd_avg_past10d", a."rejected_past10by30d_between200and1000_ratio", 
a."returned_past30d_avg_check_amount", a."rn_past30d_avg_check_amount", a."past10by30d_lessthan200_ratio"
from mrdc_score a inner join check_status b on a."mrdc_id" = b.id order by created_status
""")