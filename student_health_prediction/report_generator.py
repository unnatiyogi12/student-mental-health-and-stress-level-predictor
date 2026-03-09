from fpdf import FPDF
from datetime import datetime

def generate_report(final_stress, heart_rate, daily_steps, sleep_duration):
    

    pdf = FPDF()
    pdf.add_page()

    # Header
    pdf.set_font("Arial", "B", 18)
    pdf.cell(200,10,"AI Health Monitor Report", ln=True, align="C")

    pdf.ln(5)

    pdf.set_font("Arial", size=10)
    pdf.cell(200,10,f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align="R")

    pdf.ln(10)

    # Section title
    pdf.set_font("Arial","B",14)
    pdf.cell(200,10,"Health Summary", ln=True)

    pdf.ln(5)

    pdf.set_font("Arial", size=12)

    pdf.cell(200,8,f"Stress Level: {final_stress}", ln=True)
    pdf.cell(200,8,f"Heart Rate: {heart_rate} bpm", ln=True)
    pdf.cell(200,8,f"Daily Steps: {daily_steps}", ln=True)
    pdf.cell(200,8,f"Sleep Duration: {sleep_duration} hrs", ln=True)

    pdf.ln(10)

    # Recommendation section
    pdf.set_font("Arial","B",14)
    pdf.cell(200,10,"Recommendations", ln=True)

    pdf.set_font("Arial", size=12)

    pdf.multi_cell(0,8,
    "Maintain a healthy lifestyle by improving sleep quality, staying physically active, "
    "and managing stress through relaxation techniques like meditation or exercise.")

    file_path = "health_report.pdf"

    pdf.output(file_path)

    return file_path