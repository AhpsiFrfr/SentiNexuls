import json
from datetime import datetime
from pathlib import Path

def render_html_report(agent_outputs: dict, output_path: str = "outputs/generated_report.html"):
    """
    Convert agent pipeline outputs into a styled HTML report.
    
    Args:
        agent_outputs (dict): Results from run_agent_pipeline()
        output_path (str): Path to save the HTML report
    """
    timestamp = datetime.utcnow().isoformat()
    
    # Enhanced HTML template with better styling
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>SentiNexuls Agent Report</title>
    <style>
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; 
            padding: 40px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #004d99 0%, #0066cc 100%);
            color: white;
            padding: 30px 40px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
            font-size: 1.1em;
        }}
        .content {{
            padding: 40px;
        }}
        .section {{ 
            margin-bottom: 30px; 
            padding: 25px; 
            background: #f8f9fa; 
            border-radius: 8px; 
            border-left: 5px solid #3399ff;
            transition: transform 0.2s ease;
        }}
        .section:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        }}
        .section h2 {{ 
            color: #004d99; 
            margin-top: 0;
            font-size: 1.5em;
            text-transform: capitalize;
        }}
        .json-container {{
            background: #2d3748;
            border-radius: 6px;
            overflow: hidden;
        }}
        pre {{ 
            background: transparent;
            color: #e2e8f0;
            padding: 20px; 
            margin: 0;
            overflow-x: auto; 
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 0.9em;
            line-height: 1.5;
        }}
        .error-section {{
            border-left-color: #e53e3e;
            background: #fed7d7;
        }}
        .error-section h2 {{
            color: #c53030;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            border: 1px solid #e2e8f0;
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #3399ff;
        }}
        .stat-label {{
            color: #718096;
            font-size: 0.9em;
            margin-top: 5px;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #718096;
            border-top: 1px solid #e2e8f0;
            margin-top: 40px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ SentiNexuls Intelligence Brief</h1>
            <p>Generated: {timestamp}</p>
        </div>
        <div class="content">"""

    # Add statistics section
    if "error" not in agent_outputs:
        agent_count = len([k for k in agent_outputs.keys() if k != "error"])
        html += f"""
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">{agent_count}</div>
                    <div class="stat-label">Agents Executed</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">✅</div>
                    <div class="stat-label">Pipeline Status</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{len(str(agent_outputs))}</div>
                    <div class="stat-label">Data Points</div>
                </div>
            </div>"""

    # Add agent sections
    for agent, data in agent_outputs.items():
        section_class = "section error-section" if agent == "error" else "section"
        agent_title = "⚠️ Pipeline Error" if agent == "error" else f"🤖 {agent.replace('_', ' ').title()} Agent"
        
        html += f"""
            <div class="{section_class}">
                <h2>{agent_title}</h2>
                <div class="json-container">
                    <pre>{json.dumps(data, indent=2, ensure_ascii=False)}</pre>
                </div>
            </div>"""

    html += """
        </div>
        <div class="footer">
            <p>🔒 SentiNexuls - Advanced Threat Detection & Response Platform</p>
        </div>
    </div>
</body>
</html>"""

    # Ensure output directory exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Write HTML file
    Path(output_path).write_text(html, encoding="utf-8")
    print(f"✅ HTML report generated at {output_path}")
    return output_path

def export_pdf(html_path: str = "outputs/generated_report.html", pdf_path: str = "outputs/generated_report.pdf"):
    """
    Export HTML report to PDF using pdfkit (optional dependency).
    
    Args:
        html_path (str): Path to the HTML report
        pdf_path (str): Path to save the PDF report
    """
    try:
        import pdfkit
        
        # PDF options for better rendering
        options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None
        }
        
        # Ensure output directory exists
        Path(pdf_path).parent.mkdir(parents=True, exist_ok=True)
        
        pdfkit.from_file(html_path, pdf_path, options=options)
        print(f"📄 PDF report generated at {pdf_path}")
        return pdf_path
        
    except ImportError:
        print("⚠️ pdfkit not installed. Skipping PDF export.")
        print("💡 Install with: pip install pdfkit")
        return None
    except Exception as e:
        print(f"❌ PDF export failed: {e}")
        print("💡 Make sure wkhtmltopdf is installed on your system")
        return None

def generate_reports(agent_outputs: dict, base_name: str = "generated_report"):
    """
    Generate both HTML and PDF reports from agent pipeline outputs.
    
    Args:
        agent_outputs (dict): Results from run_agent_pipeline()
        base_name (str): Base filename for reports
        
    Returns:
        dict: Paths to generated reports
    """
    html_path = f"outputs/{base_name}.html"
    pdf_path = f"outputs/{base_name}.pdf"
    
    # Generate HTML report
    html_result = render_html_report(agent_outputs, html_path)
    
    # Attempt PDF export
    pdf_result = export_pdf(html_path, pdf_path)
    
    return {
        "html": html_result,
        "pdf": pdf_result
    }

# Usage example:
# from report_renderer import generate_reports
# reports = generate_reports(pipeline_results)
# print(f"Reports generated: {reports}") 