from fpdf import FPDF
import os

# Ensure output/ folder exists
os.makedirs("output", exist_ok=True)

# Step 1: Read the score saved from risk_model.py
with open('output/final_score.txt', 'r') as file:
    final_score = float(file.read().strip())

# Step 2: Generate Loan Recommendation based on score
if final_score >= 80:
    recommendation = "Loan Recommendation: Eligible for fast-track approval."
elif final_score >= 60:
    recommendation = "Loan Recommendation: Needs review by financial officer."
elif final_score >= 40:
    recommendation = "Loan Recommendation: Unlikely to approve without more documents."
else:
    recommendation = "Loan Recommendation: Rejected due to high financial risk."

# Step 3: LLM-style classification paragraph
summary = (
    "Account A demonstrates moderate financial stability. "
    "While the account maintains a steady inflow of funds, occasional irregularities in spending "
    "and a lower average balance indicate moderate risk. The assigned credit-worthiness score reflects this evaluation."
)

# Step 4: Generate PDF
pdf = FPDF()
pdf.add_page()

pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Account Credit-Worthiness Report", ln=True, align='C')

pdf.ln(20)
pdf.set_font("Arial", "", 14)
pdf.cell(0, 10, f"Credit-Worthiness Score: {final_score} / 100", ln=True)

pdf.ln(10)
pdf.set_font("Arial", "", 12)
pdf.multi_cell(0, 10, "Summary:\n" + summary)

pdf.ln(10)
pdf.multi_cell(0, 10, recommendation)

# Step 5: Save PDF to output/
pdf.output("output/credit_report.pdf")

print("PDF generated successfully: output/credit_report.pdf")
