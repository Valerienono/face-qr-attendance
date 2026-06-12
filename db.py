import sqlite3
from datetime import datetime

DB_NAME = "attendance.db"

OFFICE_START = "07:30:00"

    # ================= ATTENDANCE =================

def save_attendance(worker_id, name):
    print("DB.PY CALLED")

    conn = sqlite3.connect(
    DB_NAME,
    timeout=10
    )
    c = conn.cursor()

 
    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%H:%M:%S")

    c.execute("""
    SELECT rowid, check_in, check_out
    FROM attendance
    WHERE id=? AND date=?
    """, (worker_id, today))

    record = c.fetchone()

    if record is None:

        status = "ON TIME"

        if now > OFFICE_START:
            status = "LATE"

        c.execute("""
        INSERT INTO attendance
        (id, name, check_in, check_out, date, status, work_hours)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            worker_id,
            name,
            now,
            "",
            today,
            status,
            ""
        ))

        result = f"CHECK_IN:{name}"

    else:

        rowid = record[0]
        check_in = record[1]
        check_out = record[2]

        if check_out == "":

            checkin_time = datetime.strptime(
                today + " " + check_in,
                "%Y-%m-%d %H:%M:%S"
            )

            checkout_time = datetime.strptime(
                today + " " + now,
                "%Y-%m-%d %H:%M:%S"
            )

            hours = checkout_time - checkin_time

            c.execute("""
            UPDATE attendance
            SET check_out=?, work_hours=?
            WHERE rowid=?
            """, (
                now,
                str(hours),
                rowid
            ))

            result = f"CHECK_OUT:{name}"

        else:
            result = "ALREADY_OUT"

    conn.commit()
    conn.close()

    return result

    # ================= RECORD =================

def get_all_records():

    conn = sqlite3.connect(
    DB_NAME,
    timeout=10
    )
    c = conn.cursor()

    c.execute("""
    SELECT
    id,
    name,
    check_in,
    check_out,
    date,
    status,
    work_hours
    FROM attendance
    ORDER BY date DESC
    """)

    rows = c.fetchall()

    conn.close()

    return rows

    # ================= ABSENT =================

def get_absent_today(workers):

    conn = sqlite3.connect(
    DB_NAME,
    timeout=10
    )
    c = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")

    all_workers = set(workers.keys())

    c.execute("""
    SELECT DISTINCT id
    FROM attendance
    WHERE date=?
    """, (today,))

    present = set(row[0] for row in c.fetchall())

    conn.close()

    return all_workers - present

    # ================= DASHBOARD =================

def get_dashboard_data(workers):

    conn = sqlite3.connect(
    DB_NAME,
    timeout=10
    )
    c = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")

    total_workers = len(workers)

    c.execute("""
    SELECT COUNT(DISTINCT id)
    FROM attendance
    WHERE date=?
    """, (today,))

    present = c.fetchone()[0]

    c.execute("""
    SELECT COUNT(*)
    FROM attendance
    WHERE date=? AND status='LATE'
    """, (today,))

    late = c.fetchone()[0]

    absent = total_workers - present

    conn.close()

    return {
        "total_workers": total_workers,
        "present": present,
        "absent": absent,
        "late": late
    }

def init_db():
    conn = sqlite3.connect(DB_NAME, timeout=10)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id TEXT,
        name TEXT,
        check_in TEXT,
        check_out TEXT,
        date TEXT,
        status TEXT,
        work_hours TEXT
    )
    """)

    conn.commit()
    conn.close()