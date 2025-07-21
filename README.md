

<h1>📄 AI Resume Tailor</h1>

<p><strong>AI Resume Tailor</strong> is an intelligent web app that helps job seekers <strong>tailor their resume to specific job descriptions</strong> using AI. It parses resumes, identifies matched/missing keywords, and generates a personalized summary — all in a few clicks.</p>

<hr>

<h2>🚀 Features</h2>
<ul>
  <li>🔍 Resume keyword analysis</li>
  <li>📄 Job description parsing</li>
  <li>🧠 AI-generated tailored summary (via OpenRouter/GPT)</li>
  <li>✅ Highlight matched & missing keywords</li>
  <li>📤 Export reports as <code>.txt</code> and <code>.docx</code></li>
  <li>🌐 Deployed with Streamlit for public use</li>
</ul>

<hr>

<h2>🛠 How It Works (Pipeline)</h2>
<ol>
  <li><strong>Resume Upload:</strong> Supports <code>.pdf</code> and <code>.docx</code> formats. Extracts text using NLP libraries.</li>
  <li><strong>Job Description Input:</strong> Users paste any job description.</li>
  <li><strong>Keyword Comparison:</strong> Matched and missing keywords are shown in styled UI.</li>
  <li><strong>AI Tailored Summary:</strong> Uses OpenRouter API to generate a custom summary section aligned with the JD.</li>
  <li><strong>Export Options:</strong> Download a <code>.txt</code> keyword report or <code>.docx</code> AI-enhanced resume summary.</li>
</ol>

<hr>

<h2>⚙️ Tech Stack</h2>
<table>
  <tr><th>Area</th><th>Tools/Tech</th></tr>
  <tr><td>Frontend</td><td>Streamlit</td></tr>
  <tr><td>AI Generation</td><td>OpenRouter API (GPT-like models)</td></tr>
  <tr><td>Parsing</td><td>PyMuPDF, python-docx</td></tr>
  <tr><td>Backend</td><td>Python 3.x</td></tr>
  <tr><td>Export</td><td>python-docx</td></tr>
  <tr><td>Deployment</td><td>Streamlit Cloud</td></tr>
  <tr><td>Version Control</td><td>Git + GitHub</td></tr>
</table>

<hr>

<h2>🧪 Project Folder Structure</h2>

<pre>
AI-Resume-Tailor-Agent/
├── app.py                # Main Streamlit App
├── requirements.txt
├── .gitignore
├── .env                  # [Not pushed to GitHub!]
├── core/
│   ├── resume_parser.py     # Extract text from resumes
│   ├── matching_engine.py   # Compare resume vs JD
│   ├── openrouter_engine.py # Call OpenRouter API
│   ├── docx_exporter.py     # Export .docx reports
</pre>

<hr>

<h2>🔐 Why <code>.env</code> File is Not Pushed</h2>

<div class="highlight">
  The <code>.env</code> file contains sensitive secrets like:
  <pre>OPENROUTER_API_KEY=your-secret-key</pre>
</div>

<p>To protect your account and follow best practices, it is:</p>
<ul>
  <li>✅ Ignored using <code>.gitignore</code></li>
  <li>❌ Never pushed to GitHub</li>
  <li>🔐 Loaded securely using <code>python-dotenv</code></li>
</ul>

<p>
Store your API keys <strong>locally</strong> and add them to the Streamlit Cloud <a href="https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app/secrets-management" target="_blank">Secrets Manager</a> when deploying.
</p>

<hr>

<h2>📦 Setup Locally</h2>
<pre><code>git clone https://github.com/your-username/ai-resume-tailor.git
cd ai-resume-tailor
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
pip install -r requirements.txt
</code></pre>

<p><strong>Create a <code>.env</code> file and add your key:</strong></p>
<pre><code>OPENROUTER_API_KEY=your-api-key</code></pre>

<hr>

<h2>▶️ Run the App Locally</h2>
<pre><code>streamlit run app.py</code></pre>

<hr>

<h2>☁️ Deploy to Streamlit Cloud</h2>
<ol>
  <li>Push code to GitHub</li>
  <li>Go to <a href="https://streamlit.io/cloud" target="_blank">streamlit.io/cloud</a></li>
  <li>Connect your GitHub repo</li>
  <li>Set <code>app.py</code> as the entry point</li>
  <li>Add your API key under <strong>Secrets</strong></li>
</ol>

<hr>

<h2>🙌 Credits</h2>
<p>Built by <a href="https://www.linkedin.com/in/bharathsimhareddy-katta/" target="_blank">Katta Bharath Simha Reddy</a> — AI Engineer in the making 💼</p>

<hr>

<h2>📄 License</h2>
<p>This project is licensed under the <strong>MIT License</strong>.</p>

</body>
</html>
