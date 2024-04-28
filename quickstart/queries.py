# queries.py

TENANT_INFO_QUERY = """
SELECT
   t.id,
   t.first_name,
   t.last_name,
   a.apartment_number,
   l.lease_start_date,
   l.lease_end_date,
   l.rent_amount,
   t.phone,
   t.email
FROM
   quickstart_tenant t
   LEFT JOIN quickstart_lease l ON t.id = l.tenant_id
   LEFT JOIN quickstart_apartment a ON l.apartment_id = a.id
   LEFT JOIN quickstart_transaction tr ON l.id = tr.lease_id
GROUP BY
   t.id, a.apartment_number, l.lease_start_date, l.lease_end_date, l.rent_amount;
"""


ALL_TENANT_INFO_QUERY = """
SELECT
   t.id,
   t.first_name,
   t.last_name,
   t.phone,
   t.email,
   t.date_of_birth,
   t.identification_number,
   t.move_in_date,
   t.move_out_date,
   a.apartment_number,
   l.lease_start_date,
   l.lease_end_date,
   l.rent_amount
FROM
   quickstart_tenant t
   LEFT JOIN quickstart_lease l ON t.id = l.tenant_id
   LEFT JOIN quickstart_apartment a ON l.apartment_id = a.id
WHERE
   t.id = %s
"""

MONTHLY_REPORT_QUERY = """
    SELECT t.first_name, t.last_name, t.email, a.apartment_number, tr.amount_paid, tr.date,
       CASE WHEN '{}' BETWEEN l.lease_start_date AND l.lease_end_date
                THEN 1
            ELSE 0
       END as is_rented
    FROM quickstart_tenant t
    INNER JOIN quickstart_lease l ON t.id = l.tenant_id
    INNER JOIN quickstart_apartment a ON l.apartment_id = a.id
    LEFT JOIN quickstart_transaction tr ON l.id = tr.lease_id AND tr.month = {} AND tr.year = {}
    ORDER BY a.apartment_number
    LIMIT {} OFFSET {};
"""

MONTHLY_REPORT_COUNT_QUERY = """
    SELECT COUNT(*)
    FROM quickstart_tenant t
    INNER JOIN quickstart_lease l ON t.id = l.tenant_id
    INNER JOIN quickstart_apartment a ON l.apartment_id = a.id
    LEFT JOIN quickstart_transaction tr ON l.id = tr.lease_id AND tr.month = {} AND tr.year = {}
    WHERE strftime('%%Y%%m', {}) BETWEEN strftime('%%Y%%m', l.lease_start_date) AND strftime('%%Y%%m', l.lease_end_date)
"""

LEASE_TRANSACTION_REPORT_QUERY = """
SELECT COALESCE(COUNT(*), 0) as leased_apartment_count,
       COALESCE(SUM(l.rent_amount), 0) as total_rent_amount,
       COALESCE(SUM(tr.amount_paid), 0) as total_amount_paid,
       COALESCE(COUNT(tr.id), 0) as transaction_count
FROM quickstart_lease l
LEFT JOIN quickstart_transaction tr ON l.id = tr.lease_id
WHERE '{}' BETWEEN l.lease_start_date AND l.lease_end_date;
"""