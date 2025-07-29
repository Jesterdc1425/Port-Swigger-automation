from fpdf import FPDF

# Define the content of the PDF
title = "SQL Injection Detection via filterColumn with PG_SLEEP() Behavior"
content = """
Overview

During testing of a web application’s input handling for the `filterColumn` parameter, we observed non-obvious SQL injection behavior. Specifically, certain payloads yielded successful time-based SQL injection (e.g., PG_SLEEP() delays), while others gave misleading response codes like 204 No Content, despite valid SQL syntax.

This write-up outlines what we found, why it behaves this way, and how to reliably identify this kind of injection.

Injection Point: filterColumn

The parameter `filterColumn` appears to be used directly in a SQL statement like:

    SELECT <filterColumn> FROM <some_table>

This allows for the possibility of injecting entire SQL expressions in place of a column name.

Observed Behaviors

Input: "column7--" → Response: 200 OK → Appears valid, used to test comment truncation
Input: "column7--'" → Response: 204 No Content → Likely parsed as invalid; `'` after comment is ignored by SQL, but may confuse the app parser
Input: "''" → Response: 204 No Content → Valid SQL (SELECT '' FROM ...), but the app returns nothing because result may not match expected schema
Input: "(SELECT 9706 FROM PG_SLEEP(30))" → Response: 200 OK with 30s delay → ✅ Successful time-based SQL injection

Technical Explanation

- PG_SLEEP(30) causes the database to pause execution, making it useful for blind/time-based SQLi detection.
- The payload:

      (SELECT 9706 FROM PG_SLEEP(30))

  injects a full expression that the backend treats as a column in a SELECT statement.
- Although PG_SLEEP() is not traditionally used in a FROM clause, this query executes successfully, possibly due to how the SQL engine handles scalar expressions in subqueries in this app’s database context (likely PostgreSQL).

Why This Is Easy to Miss

- The app does not return explicit SQL errors.
- Certain invalid or non-matching values (like '' or malformed syntax) return 204 No Content, misleading testers into thinking SQL injection is not possible.
- Successful injection (PG_SLEEP) returns 200 OK, but only with a measurable delay — so timing must be observed.

How to Test This Properly

1. Test for Time-Based SQLi:

      "filterColumn": "(SELECT PG_SLEEP(5))"

   If response is delayed by ~5 seconds → injection confirmed.

2. Avoid False Negatives:
   Don’t assume 204 means “safe”. Even valid SQL like '' might trigger a 204 due to how the app handles empty results.

3. Try Logical Payloads:

      "filterColumn": "(SELECT CASE WHEN (1=1) THEN PG_SLEEP(5) ELSE 0 END)"

   Useful for conditional exfiltration later.

Takeaways for Pentesters

- Always test for time-based SQLi even if the app returns 204 or no visual error.
- Test payloads that replace SQL expressions, not just values.
- Be suspicious if a parameter allows raw SQL expressions (e.g., filterColumn) — this often indicates unsafe dynamic SQL.

Example Exploitation Flow

1. Confirm injection:

      "filterColumn": "(SELECT PG_SLEEP(5))"

2. Escalate to data extraction (blind SQLi):

      "filterColumn": "(SELECT CASE WHEN (SUBSTRING(current_user,1,1)='a') THEN PG_SLEEP(5) ELSE 0 END)"

3. Automate using Burp Intruder or custom scripts with timing detection.
"""

# Create PDF
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

pdf.set_font("Arial", 'B', 14)
pdf.multi_cell(0, 10, title)

pdf.ln(5)
pdf.set_font("Arial", '', 11)
pdf.multi_cell(0, 8, content)

# Save the PDF
pdf.output("SQLi_filterColumn_PG_SLEEP_Writeup.pdf")
