select *
from vw_security_posture
order by highest_open_severity desc, release_security_decision asc;
