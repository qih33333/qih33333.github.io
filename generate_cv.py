"""Generate Hao Qi's website CV as a compact, one-page PDF."""

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


OUTPUT = "tmp/pdfs/CV-new.pdf"
NAVY = colors.HexColor("#202837")
BLUE = colors.HexColor("#425c78")
COPPER = colors.HexColor("#B67B4A")
TEXT = colors.HexColor("#242A33")
MUTED = colors.HexColor("#5F6570")
RULE = colors.HexColor("#C9C5BD")

PAGE_W, PAGE_H = letter
LEFT = 0.46 * inch
RIGHT = 0.46 * inch
TOP = 0.34 * inch
BOTTOM = 0.31 * inch


class CVDocTemplate(BaseDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name == "Section":
            self.canv.bookmarkPage(flowable.getPlainText())


def page_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.35)
    canvas.line(LEFT, 0.255 * inch, PAGE_W - RIGHT, 0.255 * inch)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 6.4)
    canvas.drawString(LEFT, 0.13 * inch, "Hao Qi | Curriculum Vitae")
    canvas.drawRightString(PAGE_W - RIGHT, 0.13 * inch, f"Page {doc.page}")
    canvas.restoreState()


styles = getSampleStyleSheet()

name_style = ParagraphStyle(
    "Name",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=22,
    leading=23,
    textColor=NAVY,
    alignment=TA_CENTER,
    spaceAfter=1,
)

title_style = ParagraphStyle(
    "Title",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=9.1,
    leading=10.8,
    textColor=BLUE,
    alignment=TA_CENTER,
    spaceAfter=1,
)

contact_style = ParagraphStyle(
    "Contact",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8.0,
    leading=9.6,
    textColor=MUTED,
    alignment=TA_CENTER,
)

section_style = ParagraphStyle(
    "Section",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=10.2,
    leading=11.4,
    textColor=NAVY,
    spaceBefore=5.3,
    spaceAfter=2.5,
    borderWidth=0,
)

school_style = ParagraphStyle(
    "School",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=8.65,
    leading=10.1,
    textColor=TEXT,
)

right_style = ParagraphStyle(
    "Right",
    parent=school_style,
    fontName="Helvetica",
    alignment=TA_RIGHT,
    textColor=MUTED,
)

body_style = ParagraphStyle(
    "Body",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8.05,
    leading=9.7,
    textColor=TEXT,
    alignment=TA_LEFT,
)

small_style = ParagraphStyle(
    "Small",
    parent=body_style,
    fontSize=7.55,
    leading=9.0,
    textColor=MUTED,
)

bullet_style = ParagraphStyle(
    "Bullet",
    parent=body_style,
    leftIndent=11,
    firstLineIndent=-6,
    bulletIndent=3,
    spaceAfter=0.6,
)

publication_style = ParagraphStyle(
    "Publication",
    parent=body_style,
    leftIndent=10,
    firstLineIndent=-6,
    bulletIndent=2,
    fontSize=7.75,
    leading=9.25,
    spaceAfter=2.1,
)


def section(title):
    label = Paragraph(title.upper(), section_style)
    line = Table([[label]], colWidths=[PAGE_W - LEFT - RIGHT])
    line.setStyle(
        TableStyle(
            [
                ("LINEBELOW", (0, 0), (-1, -1), 0.6, NAVY),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1.3),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    return KeepTogether([line, Spacer(1, 1.6)])


def two_col(left_text, right_text, left_style=school_style, right=right_style):
    table = Table(
        [[Paragraph(left_text, left_style), Paragraph(right_text, right)]],
        colWidths=[5.62 * inch, 1.46 * inch],
    )
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    return table


def bullet(text, style=bullet_style):
    return Paragraph(f"• {text}", style)


story = [
    Paragraph("HAO QI", name_style),
    Paragraph("Ph.D. Student in Applied Mathematics (Statistics) · UNC Charlotte", title_style),
    Paragraph(
        '+1 910-998-5536 &nbsp;|&nbsp; <link href="mailto:hqi1@charlotte.edu" color="#425C78">hqi1@charlotte.edu</link> &nbsp;|&nbsp; Charlotte, NC 28223 &nbsp;|&nbsp; <link href="https://qih33333.github.io/" color="#425C78">qih33333.github.io</link>',
        contact_style,
    ),
    Spacer(1, 2.5),
    section("Education"),
]

education = [
    (
        "University of North Carolina at Charlotte (UNC Charlotte)",
        "Charlotte, NC",
        "Ph.D. in Applied Mathematics (Statistics Concentration) · Advisor: Dr. Qingning Zhou",
        "08/2026 - Present",
    ),
    (
        "Rice University",
        "Houston, TX",
        "Master of Statistics · GPA: 3.96/4.00",
        "08/2024 - 12/2025",
    ),
    (
        "University of North Carolina Wilmington (UNCW)",
        "Wilmington, NC",
        "B.S. in Mathematics (Statistics Minor) · GPA: 3.94/4.00 · Dean's List",
        "08/2023 - 05/2024",
    ),
    (
        "Chongqing University of Arts and Sciences (CUAS)",
        "Chongqing, China",
        "B.S. in Mathematics and Applied Mathematics · GPA: 91.1/100 · Rank: 1/95",
        "09/2020 - 06/2024",
    ),
]

for school, location, degree, dates in education:
    story.extend(
        [
            two_col(school, location),
            two_col(f"• &nbsp;{degree}", dates, body_style, right_style),
            Spacer(1, 1.2),
        ]
    )

story.extend(
    [
        section("Publications"),
        bullet(
            "Xinjie Lan, Yunbo Mei, Leheng Zhou, <b>Hao Qi</b>, Shichen Tang, and Yunli Su. “Bayesian Time-aware Attention: Enhancing Transformers for Non-Stationary Time Series Forecasting.” Manuscript submitted to AAAI, 2026.",
            publication_style,
        ),
        bullet(
            'Travis J. Miles, Michael T. Guinn, Xin Tan, <b>Hao Qi</b>, Vicente Orozco-Sevilla, Marc R. Moon, et al. “Tissue perfusion pressure: A novel hemodynamic measure to assess risk of acute kidney injury after cardiac surgery.” <i>J. Thorac. Cardiovasc. Surg.</i>, 171(2):455-462.e3, 2026. <link href="https://doi.org/10.1016/j.jtcvs.2025.07.009" color="#425C78">doi:10.1016/j.jtcvs.2025.07.009</link>.',
            publication_style,
        ),
        bullet(
            '<b>Hao Qi</b> and Yuanshen Wang. “Prediction and Analysis of Stock Logarithmic Returns Based on ARMA-GARCH Model.” <i>Proceedings of CECNet 2022</i>. <link href="https://doi.org/10.3233/FAIA220575" color="#425C78">doi:10.3233/FAIA220575</link>.',
            publication_style,
        ),
        bullet(
            '<b>Hao Qi</b>. “Research on Forecasting for Different Types of Small Sample Time Series Data.” <i>2022 6th Annual International Conference on Data Science and Business Analytics (ICDSBA)</i>. <link href="https://doi.org/10.1109/ICDSBA57203.2022.00035" color="#425C78">doi:10.1109/ICDSBA57203.2022.00035</link>.',
            publication_style,
        ),
        section("Research Experience"),
        two_col(
            "Longitudinal Variational Autoencoder for Within-Subject Image Prediction, Rice University",
            "02/2026 - Present",
        ),
        Paragraph("Supervised by Dr. Huixia Judy Wang (Rice University)", small_style),
        bullet("Developed a longitudinal variational autoencoder with a mixed-effects latent backbone and a first-order stochastic transition to model subject-specific temporal dynamics in image sequences."),
        bullet("Reformulated the task as prefix-conditioned missing-visit prediction, generating each visit from observed prior visits under a sequential latent-variable framework."),
        bullet("Derived an ELBO-based objective and evaluated one-step and recursive forecasting performance on longitudinal imaging data."),
        Spacer(1, 1.2),
        two_col(
            "A Novel Hemodynamic Measure to Assess Risk of Acute Kidney Injury After Cardiac Surgery, Rice &amp; BCM",
            "02/2025 - 07/2025",
        ),
        Paragraph("Supervised by Dr. Meng Li (Rice University)", small_style),
        bullet("Applied univariate and multivariable logistic regression to quantify the association between tissue perfusion pressure (TPP) and postoperative acute kidney injury (AKI), with analyses stratified by vasoactive inotrope score."),
        bullet("Identified a 38 mm Hg TPP threshold using regression-based risk estimation and demonstrated that TPP below this level remained an independent predictor after statistical adjustment."),
        bullet("Conducted prespecified sensitivity and subgroup analyses that yielded consistent effect estimates."),
        section("Work Experience"),
        two_col("Rice University · Research Assistant (with Dr. Meng Li)", "01/2026 - 06/2026"),
        bullet("Developed dynamic machine-learning models to predict acute kidney injury after cardiac surgery using hemodynamics, laboratory measurements, medications, and clinical data."),
        bullet("Implemented rolling-window feature extraction and evaluated XGBoost, random forest, and logistic regression under strict patient-level data splits."),
        bullet("Built calibration-based evaluation metrics, mapped predicted creatinine to KDIGO AKI stages, and conducted external validation using the MIMIC dataset."),
        section("Awards and Honors"),
        Paragraph("China National Scholarship &nbsp;&nbsp;·&nbsp;&nbsp; Chongqing Outstanding College Graduate Student", body_style),
        section("Skills"),
        Paragraph("<b>Programming:</b> Python, R, MATLAB, SAS &nbsp;&nbsp;|&nbsp;&nbsp; <b>Tools:</b> Word, Excel, PowerPoint, LaTeX &nbsp;&nbsp;|&nbsp;&nbsp; <b>Languages:</b> Mandarin (native), English (senior)", body_style),
    ]
)

doc = CVDocTemplate(
    OUTPUT,
    pagesize=letter,
    leftMargin=LEFT,
    rightMargin=RIGHT,
    topMargin=TOP,
    bottomMargin=BOTTOM,
    title="Hao Qi - Curriculum Vitae",
    author="Hao Qi",
    subject="Academic curriculum vitae",
)

frame = Frame(
    LEFT,
    BOTTOM + 0.04 * inch,
    PAGE_W - LEFT - RIGHT,
    PAGE_H - TOP - BOTTOM - 0.04 * inch,
    leftPadding=0,
    rightPadding=0,
    topPadding=0,
    bottomPadding=0,
)
doc.addPageTemplates([PageTemplate(id="CV", frames=[frame], onPage=page_footer)])
doc.build(story)

print(OUTPUT)
