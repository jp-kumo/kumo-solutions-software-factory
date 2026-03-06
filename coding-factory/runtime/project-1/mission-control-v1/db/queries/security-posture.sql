select *
from vw_security_posture
order by highest_open_severity desc, reviewed_at nulls first;
