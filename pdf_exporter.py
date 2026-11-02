import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_post_pdf(post_title, topic, variation, length, language, tone, model, quality_score, content):
    """
    Generates a beautifully formatted PDF document for the generated LinkedIn post.
    Returns bytes buffer ready for st.download_button.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Brand Palette
    primary_color = colors.HexColor("#6366F1")    # Indigo / Violet
    dark_color = colors.HexColor("#0F172A")       # Slate 900
    subtext_color = colors.HexColor("#64748B")    # Slate 500
    card_bg = colors.HexColor("#F8FAFC")          # Slate 50
    border_color = colors.HexColor("#E2E8F0")     # Slate 200
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=primary_color,
        spaceAfter=4
    )
    
    meta_style = ParagraphStyle(
        'MetaStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=subtext_color
    )
    
    body_style = ParagraphStyle(
        'PostContent',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=17,
        textColor=dark_color,
        spaceAfter=8
    )
    
    footer_style = ParagraphStyle(
        'FooterStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=10,
        textColor=subtext_color,
        alignment=1 # Center
    )
    
    story = []
    
    # Title & Badge
    story.append(Paragraph("NexPost AI — Enterprise Content Export", title_style))
    story.append(Paragraph(f"Created by <b>Kartikey Sabharwal</b> &bull; Capstone Generative AI Studio", meta_style))
    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=14))
    
    # Metadata Summary Table
    meta_data = [
        [
            Paragraph(f"<b>Topic:</b> {topic}", meta_style),
            Paragraph(f"<b>Style Variation:</b> {variation}", meta_style),
            Paragraph(f"<b>Length:</b> {length}", meta_style)
        ],
        [
            Paragraph(f"<b>Language:</b> {language}", meta_style),
            Paragraph(f"<b>Tone:</b> {tone}", meta_style),
            Paragraph(f"<b>Quality Score:</b> {quality_score}%", meta_style)
        ],
        [
            Paragraph(f"<b>AI Model:</b> {model}", meta_style),
            Paragraph("<b>Target Platform:</b> LinkedIn", meta_style),
            Paragraph("<b>In-Context:</b> Few-Shot Conditioned", meta_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[175, 175, 175])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), card_bg),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('INNERGRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 16))
    
    # Post Heading
    story.append(Paragraph("<b>Synthesized LinkedIn Post:</b>", ParagraphStyle(
        'SubHeader', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=13, textColor=dark_color
    )))
    story.append(Spacer(1, 8))
    
    # Clean text and paragraphs
    clean_content = content.replace("<br>", "\n").replace("&", "&amp;")
    paras = clean_content.split("\n")
    for p in paras:
        p_strip = p.strip()
        if p_strip:
            story.append(Paragraph(p_strip, body_style))
        else:
            story.append(Spacer(1, 6))
            
    story.append(Spacer(1, 25))
    story.append(HRFlowable(width="100%", thickness=0.8, color=border_color, spaceAfter=10))
    story.append(Paragraph("&copy; 2026 Kartikey Sabharwal &bull; NexPost AI Studio &bull; All Rights Reserved", footer_style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
