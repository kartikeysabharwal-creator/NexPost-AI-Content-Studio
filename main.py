import streamlit as st
import os
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

from few_shot import FewShotPosts
import post_generator
from llm_helper import AVAILABLE_MODELS, DEFAULT_MODEL
import db_helper
from pdf_exporter import generate_post_pdf

# 1. Page Configuration
st.set_page_config(
    page_title="NexPost AI | Generative AI Studio",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Modern Cyberpunk / Electric Indigo Theme (Original, Custom Palette)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        --primary-indigo: #6366F1;
        --accent-violet: #8B5CF6;
        --neon-cyan: #06B6D4;
        --bg-surface: #0F172A;
        --card-dark: #1E293B;
        --card-border: #334155;
        --text-pure: #F8FAFC;
        --text-sub: #94A3B8;
    }
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4, .brand-title {
        font-family: 'Space Grotesk', sans-serif !important;
    }
    
    /* Header Gradient & Badge */
    .brand-title {
        background: linear-gradient(135deg, #A855F7 0%, #6366F1 50%, #06B6D4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        margin-bottom: 0.2rem;
    }
    
    .creator-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: linear-gradient(90deg, rgba(99, 102, 241, 0.15), rgba(168, 85, 247, 0.15));
        border: 1px solid rgba(99, 102, 241, 0.4);
        padding: 5px 14px;
        border-radius: 9999px;
        color: #C084FC;
        font-weight: 600;
        font-size: 0.82rem;
        letter-spacing: 0.02em;
        margin-bottom: 0.8rem;
    }
    
    /* Score Metric Tiles */
    .score-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 12px;
        padding: 14px;
        text-align: center;
        backdrop-filter: blur(8px);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .score-card:hover {
        border-color: #6366F1;
        transform: translateY(-2px);
    }
    
    .score-val {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #38BDF8;
    }
    
    .score-lbl {
        font-size: 0.72rem;
        font-weight: 600;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-top: 2px;
    }
    
    /* Professional LinkedIn Simulation Card */
    .li-preview-container {
        background: #FFFFFF;
        color: #191919;
        border-radius: 14px;
        padding: 22px 26px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
        border: 1px solid #E2E8F0;
        margin-top: 10px;
        margin-bottom: 15px;
    }
    
    .li-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 12px;
    }
    
    .li-avatar {
        width: 46px;
        height: 46px;
        border-radius: 50%;
        background: linear-gradient(135deg, #6366F1, #8B5CF6);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 700;
        font-size: 1.1rem;
        flex-shrink: 0;
    }
    
    .li-meta-name {
        font-weight: 700;
        font-size: 0.95rem;
        color: #0F172A;
    }
    
    .li-meta-bio {
        font-size: 0.78rem;
        color: #64748B;
        line-height: 1.2;
    }
    
    .li-content-text {
        white-space: pre-wrap;
        font-size: 0.96rem;
        line-height: 1.65;
        color: #1E293B;
        margin: 14px 0;
    }
    
    .li-actions-bar {
        border-top: 1px solid #F1F5F9;
        padding-top: 12px;
        display: flex;
        gap: 24px;
        font-size: 0.85rem;
        font-weight: 600;
        color: #64748B;
    }
    
    /* Model Comparison Pill */
    .model-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 6px;
        background: rgba(99, 102, 241, 0.18);
        color: #818CF8;
        font-size: 0.75rem;
        font-weight: 600;
        font-family: monospace;
    }
    
    /* Global Footer */
    .app-footer {
        text-align: center;
        padding: 30px 0 15px 0;
        color: #94A3B8;
        font-size: 0.88rem;
        border-top: 1px solid rgba(148, 163, 184, 0.15);
        margin-top: 40px;
    }
    .app-footer strong {
        color: #C084FC;
    }
</style>
""", unsafe_allow_html=True)

# 3. Cache & Database Loading
@st.cache_resource
def get_dataset():
    return FewShotPosts()

fs = get_dataset()

# 4. Session State Management
if "generated_variations" not in st.session_state:
    st.session_state.generated_variations = None
if "selected_variation_tab" not in st.session_state:
    st.session_state.selected_variation_tab = "Professional"
if "rewrite_result" not in st.session_state:
    st.session_state.rewrite_result = None
if "active_topic" not in st.session_state:
    st.session_state.active_topic = "Career Advice"

# 5. Sidebar Controls & Customization
with st.sidebar:
    st.markdown('<div style="text-align:center; padding-bottom: 10px;"><span style="font-size: 42px;">⚡</span></div>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; margin-bottom: 2px;'>NexPost AI</h2>", unsafe_allow_html=True)
    st.caption("<div style='text-align:center;'>Generative AI Studio &bull; Final Year Capstone</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("⚙️ Inference Engine")
    
    selected_model = st.selectbox(
        "Active Groq Model",
        options=AVAILABLE_MODELS,
        index=0,
        help="Ultra-fast Groq LPU models."
    )
    
    creativity = st.slider(
        "Temperature (Creativity)",
        min_value=0.1,
        max_value=1.1,
        value=0.7,
        step=0.05,
        help="Higher values spark novel phrasing, lower values maximize precision."
    )
    
    st.markdown("---")
    st.subheader("🔑 Engine Authentication")
    current_key = os.getenv("GROQ_API_KEY", "")
    if current_key:
        masked_key = current_key[:7] + "..." + current_key[-4:]
        st.success(f"Groq API Active: `{masked_key}`")
    else:
        user_key = st.text_input("Enter Groq API Key", type="password")
        if user_key:
            os.environ["GROQ_API_KEY"] = user_key
            st.rerun()

    st.markdown("---")
    with st.expander("👨‍🎓 Creator & Project Credits", expanded=True):
        st.markdown("""
        **Developer & Creator**:  
        **Kartikey Sabharwal**  
        
        **Project**:  
        NexPost AI — Enterprise In-Context Generative Studio  
        
        **Submission**:  
        Final Year Capstone Project  
        Department of Computer Science & Engineering
        """)

# 6. Main App Header Banner
head_c1, head_c2 = st.columns([3, 1.2])
with head_c1:
    st.markdown('<div class="creator-pill">✨ Developed & Engineered by <b>Kartikey Sabharwal</b></div>', unsafe_allow_html=True)
    st.markdown('<h1 class="brand-title">NexPost AI Content Studio</h1>', unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8; font-size: 1.05rem; margin-top: -6px;'>Next-generation LinkedIn post synthesizer powered by Groq LPUs, Few-Shot In-Context Learning, and real-time Quality Scoring.</p>", unsafe_allow_html=True)

with head_c2:
    db_stats = db_helper.get_history_summary()
    st.markdown(f"""
    <div class="score-card" style="margin-top: 15px; border-color: rgba(99, 102, 241, 0.4);">
        <div class="score-val" style="color: #A855F7;">{db_stats['total_posts']}</div>
        <div class="score-lbl">Synthesized Posts Recorded</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

# 7. Core Application Tabs
tab_generator, tab_rewriter, tab_model_compare, tab_analytics, tab_dataset, tab_defense = st.tabs([
    "🚀 3-Variation Generator",
    "✍️ AI Content Rewriter",
    "⚡ Model Comparison & Latency",
    "📊 Performance Dashboard",
    "📚 Exemplar Knowledge Base",
    "🎓 Viva & Technical Architecture"
])

# ==============================================================================
# TAB 1: 3-VARIATION GENERATOR STUDIO
# ==============================================================================
with tab_generator:
    st.markdown("### 1. Configure Post Generation Directives")
    
    col_input1, col_input2, col_input3, col_input4 = st.columns([1.3, 1, 1, 1])
    
    raw_tags = fs.get_tags()
    tag_options = raw_tags + ["+ Custom Topic..."]
    
    with col_input1:
        sel_tag_opt = st.selectbox("🎯 Core Topic / Domain", options=tag_options, index=0)
        if sel_tag_opt == "+ Custom Topic...":
            chosen_topic = st.text_input("Enter Custom Topic", placeholder="e.g., Generative AI in Healthcare")
        else:
            chosen_topic = sel_tag_opt
            
    with col_input2:
        chosen_length = st.selectbox(
            "📏 Post Length",
            options=["Short", "Medium", "Long"],
            index=1,
            help="Short (<50 words), Medium (50-120 words), Long (120-250 words story)"
        )
        
    with col_input3:
        chosen_language = st.selectbox(
            "🌐 Language Script",
            options=["English", "Hinglish"],
            index=0,
            help="Hinglish seamlessly blends popular Hindi expressions in Roman script."
        )
        
    with col_input4:
        chosen_tone = st.selectbox(
            "🎭 Base Emotion / Tone",
            options=["Professional", "Storytelling", "Motivational", "Contrarian / Bold", "Humorous / Relatable", "Educational"],
            index=0
        )
        
    with st.expander("🎯 Persona & Audience Fine-Tuning (Optional)", expanded=False):
        c_p1, c_p2 = st.columns(2)
        with c_p1:
            target_audience = st.text_input("Target Audience Persona", value="Tech Professionals, Engineers & Recruiters")
        with c_p2:
            custom_directive = st.text_input("Specific Angle or Key Takeaway", placeholder="e.g., Emphasize practical portfolio projects over certificates")

    col_gen_btn, _ = st.columns([1.6, 3])
    with col_gen_btn:
        generate_clicked = st.button("✨ Synthesize 3 AI Variations", type="primary", use_container_width=True)

    if generate_clicked:
        if not chosen_topic:
            st.error("Please specify a valid topic.")
        else:
            with st.spinner("Synthesizing 3 distinct AI post variations on Groq LPU..."):
                try:
                    variations = post_generator.generate_all_variations(
                        length=chosen_length,
                        language=chosen_language,
                        tag=chosen_topic,
                        tone=chosen_tone,
                        audience=target_audience,
                        custom_prompt=custom_directive,
                        model_name=selected_model,
                        temperature=creativity
                    )
                    st.session_state.generated_variations = variations
                    st.session_state.active_topic = chosen_topic
                    
                    # Save each generated variation to SQLite
                    for v_type, data in variations.items():
                        db_helper.save_post(
                            topic=chosen_topic,
                            length=chosen_length,
                            language=chosen_language,
                            tone=chosen_tone,
                            variation_type=v_type,
                            post_content=data["content"],
                            model_name=selected_model,
                            metrics=data["metrics"]
                        )
                    st.toast("Generated 3 diverse styles & saved to SQLite database!", icon="🔥")
                except Exception as e:
                    st.error(f"Error during post generation: {e}")

    # Display Variation Results
    if st.session_state.generated_variations:
        st.markdown("---")
        st.markdown("### 2. Multi-Variation Output & Quality Analysis")
        
        var_tabs = st.tabs([
            "👔 Variation A: Professional",
            "📖 Variation B: Storytelling",
            "⚡ Variation C: Engaging & Viral"
        ])
        
        variation_keys = ["Professional", "Storytelling", "Engaging"]
        
        for idx, v_key in enumerate(variation_keys):
            with var_tabs[idx]:
                v_data = st.session_state.generated_variations[v_key]
                v_content = v_data["content"]
                v_metrics = v_data["metrics"]
                
                content_col, metrics_col = st.columns([1.8, 1.2])
                
                with content_col:
                    st.markdown(f"**Style:** `{post_generator.VARIATION_PERSONAS[v_key]['title']}`")
                    st.caption(post_generator.VARIATION_PERSONAS[v_key]['description'])
                    
                    # LinkedIn Live Simulation Card
                    st.markdown(f"""
                    <div class="li-preview-container">
                        <div class="li-header">
                            <div class="li-avatar">KS</div>
                            <div>
                                <div class="li-meta-name">Kartikey Sabharwal</div>
                                <div class="li-meta-bio">AI Engineer &bull; NexPost AI Creator &bull; Final Year Capstone</div>
                                <div style="font-size: 0.72rem; color: #94A3B8;">Just now &bull; 🌐 Public</div>
                            </div>
                        </div>
                        <div class="li-content-text">{v_content}</div>
                        <div class="li-actions-bar">
                            <span>👍 Like</span>
                            <span>💬 Comment</span>
                            <span>🔁 Repost</span>
                            <span>📤 Send</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Action Buttons: One-Click Copy & PDF Download
                    act_c1, act_c2 = st.columns(2)
                    with act_c1:
                        st.download_button(
                            label="📄 Download Post PDF",
                            data=generate_post_pdf(
                                post_title=f"NexPost - {v_key}",
                                topic=st.session_state.active_topic,
                                variation=v_key,
                                length=chosen_length,
                                language=chosen_language,
                                tone=chosen_tone,
                                model=selected_model,
                                quality_score=v_metrics["overall_score"],
                                content=v_content
                            ),
                            file_name=f"NexPost_{v_key}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    with act_c2:
                        with st.expander("📋 One-Click Copy", expanded=False):
                            st.code(v_content, language="markdown")

                with metrics_col:
                    st.markdown("##### 🔍 Transparent Quality Scorecard")
                    
                    # 4 Score Tiles
                    s1, s2 = st.columns(2)
                    with s1:
                        st.markdown(f"""
                        <div class="score-card">
                            <div class="score-val" style="color: #6366F1;">{v_metrics['overall_score']}%</div>
                            <div class="score-lbl">Quality Score</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with s2:
                        st.markdown(f"""
                        <div class="score-card">
                            <div class="score-val" style="color: #10B981;">{v_metrics['latency']}s</div>
                            <div class="score-lbl">Response Time</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
                    
                    s3, s4 = st.columns(2)
                    with s3:
                        st.markdown(f"""
                        <div class="score-card">
                            <div class="score-val" style="color: #F59E0B;">{v_metrics['words']}</div>
                            <div class="score-lbl">Word Count</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with s4:
                        st.markdown(f"""
                        <div class="score-card">
                            <div class="score-val" style="color: #EC4899;">~{v_metrics['read_time_seconds']}s</div>
                            <div class="score-lbl">Read Time</div>
                        </div>
                        """, unsafe_allow_html=True)

                    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
                    st.markdown("**Metric Factor Breakdown:**")
                    st.progress(v_metrics["hook_score"] / 100, text=f"Opening Hook Impact: {v_metrics['hook_score']}%")
                    st.progress(v_metrics["readability_score"] / 100, text=f"Readability & Line Pacing: {v_metrics['readability_score']}%")
                    st.progress(v_metrics["cta_score"] / 100, text=f"Call to Action (CTA) Clarity: {v_metrics['cta_score']}%")
                    st.progress(v_metrics["hashtag_score"] / 100, text=f"Hashtags & SEO Density: {v_metrics['hashtag_score']}%")


# ==============================================================================
# TAB 2: AI CONTENT REWRITER & POLISHER
# ==============================================================================
with tab_rewriter:
    st.markdown("### ✍️ AI Content Rewriter & Quality Enhancer")
    st.caption("Transform any draft post using specialized prompt engineering to sharpen hooks, fix flow, or optimize for engagement.")
    
    col_rw_in, col_rw_out = st.columns(2)
    
    with col_rw_in:
        st.markdown("##### 📝 Input Draft Post")
        default_draft = ""
        if st.session_state.generated_variations:
            default_draft = st.session_state.generated_variations["Professional"]["content"]
            
        rewrite_input = st.text_area(
            "Draft Content to Polish",
            value=default_draft,
            height=260,
            placeholder="Paste any rough post or draft here..."
        )
        
        col_goal, col_temp = st.columns([1.5, 1])
        with col_goal:
            rewrite_goal = st.selectbox(
                "Rewriting Objective",
                options=[
                    "Sharpen Opening Hook",
                    "Fix Grammar & Flow",
                    "Optimize for Viral Engagement",
                    "Condense & Make Punchy",
                    "Enhance Hashtags & SEO",
                    "Translate to Natural Hinglish"
                ]
            )
        with col_temp:
            rw_custom_note = st.text_input("Custom Guidance (Optional)", placeholder="e.g. Add 2 bullet points")
            
        if st.button("🚀 Rewrite & Enhance Post", type="primary", use_container_width=True):
            if not rewrite_input.strip():
                st.error("Please enter text to rewrite.")
            else:
                with st.spinner(f"Rewriting using objective: '{rewrite_goal}'..."):
                    try:
                        rewritten_text, rw_latency = post_generator.rewrite_content(
                            original_text=rewrite_input,
                            rewrite_goal=rewrite_goal,
                            custom_instruction=rw_custom_note,
                            model_name=selected_model,
                            temperature=creativity
                        )
                        st.session_state.rewrite_result = {
                            "text": rewritten_text,
                            "latency": rw_latency,
                            "goal": rewrite_goal
                        }
                        db_helper.save_rewrite(
                            goal=rewrite_goal,
                            original_text=rewrite_input,
                            rewritten_text=rewritten_text,
                            model_name=selected_model,
                            latency=rw_latency
                        )
                        st.toast(f"Post rewritten in {rw_latency}s!", icon="✨")
                    except Exception as e:
                        st.error(f"Error during rewriting: {e}")

    with col_rw_out:
        st.markdown("##### 🌟 Polished & Enhanced Output")
        if st.session_state.rewrite_result:
            rw_res = st.session_state.rewrite_result
            st.markdown(f"**Applied Transformation:** `{rw_res['goal']}` &bull; Latency: `{rw_res['latency']}s`")
            
            st.markdown(f"""
            <div class="li-preview-container">
                <div class="li-header">
                    <div class="li-avatar" style="background: linear-gradient(135deg, #10B981, #06B6D4);">AI</div>
                    <div>
                        <div class="li-meta-name">Kartikey Sabharwal (Polished Post)</div>
                        <div class="li-meta-bio">AI Refined Content &bull; NexPost AI Studio</div>
                    </div>
                </div>
                <div class="li-content-text">{rw_res['text']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("📋 Copy Rewritten Text", expanded=True):
                st.code(rw_res["text"], language="markdown")
        else:
            st.info("Select a rewriting goal on the left and click **Rewrite & Enhance Post** to preview results.")


# ==============================================================================
# TAB 3: MODEL COMPARISON & RESPONSE-TIME BENCHMARK
# ==============================================================================
with tab_model_compare:
    st.markdown("### ⚡ Live AI Model Benchmark & Response-Time Comparison")
    st.caption("Benchmark multiple Groq models side-by-side on the same prompt to evaluate latency, token velocity, and content quality.")
    
    col_bench_prompt, col_bench_models = st.columns([2, 1])
    with col_bench_prompt:
        bench_topic = st.text_input("Benchmark Topic", value=st.session_state.active_topic)
    with col_bench_models:
        bench_length = st.selectbox("Benchmark Length", ["Short", "Medium"], index=0)
        
    if st.button("🏁 Run Multi-Model Benchmark Test", type="primary"):
        models_to_test = ["openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3.8-27b"]
        benchmark_results = []
        
        prog_bar = st.progress(0, text="Starting benchmark...")
        
        for i, m_name in enumerate(models_to_test):
            prog_bar.progress((i + 1) / len(models_to_test), text=f"Benchmarking {m_name}...")
            try:
                start_t = time.time()
                res = post_generator.generate_variation(
                    variation_type="Professional",
                    length=bench_length,
                    language="English",
                    tag=bench_topic,
                    tone="Professional",
                    model_name=m_name,
                    temperature=0.7
                )
                lat = res["metrics"]["latency"]
                benchmark_results.append({
                    "Model": m_name,
                    "Latency (s)": lat,
                    "Quality Score": res["metrics"]["overall_score"],
                    "Words": res["metrics"]["words"],
                    "Sample Hook": res["content"].split("\n")[0][:60] + "..."
                })
            except Exception as e:
                benchmark_results.append({
                    "Model": m_name,
                    "Latency (s)": 0,
                    "Quality Score": 0,
                    "Words": 0,
                    "Sample Hook": f"Failed: {e}"
                })
        prog_bar.empty()
        
        b_df = pd.DataFrame(benchmark_results)
        
        c_b1, c_b2 = st.columns(2)
        with c_b1:
            fig_lat = px.bar(
                b_df, x="Model", y="Latency (s)",
                color="Latency (s)",
                color_continuous_scale="Purples",
                title="Response-Time Latency (Lower is Faster)",
                text_auto=True
            )
            fig_lat.update_layout(template="plotly_dark")
            st.plotly_chart(fig_lat, use_container_width=True)
            
        with c_b2:
            fig_qs = px.bar(
                b_df, x="Model", y="Quality Score",
                color="Quality Score",
                color_continuous_scale="Viridis",
                title="Content Quality Score Index (Out of 100)",
                text_auto=True
            )
            fig_qs.update_layout(template="plotly_dark")
            st.plotly_chart(fig_qs, use_container_width=True)
            
        st.dataframe(b_df, use_container_width=True)


# ==============================================================================
# TAB 4: SQLITE DATABASE & ANALYTICS DASHBOARD
# ==============================================================================
with tab_analytics:
    st.markdown("### 📊 Persistent Generation History & Plotly Analytics")
    st.caption("Every generation is automatically recorded in the local SQLite database (`nexpost.db`) for academic verification.")
    
    posts_data = db_helper.get_all_posts(limit=100)
    
    if not posts_data:
        st.info("No records in database yet. Generate posts in the Generator tab to populate analytics.")
    else:
        df_history = pd.DataFrame(posts_data)
        
        # Summary KPI Row
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        with kpi1:
            st.metric("Total Generated Posts", len(df_history))
        with kpi2:
            st.metric("Average Quality Score", f"{df_history['quality_score'].mean():.1f}%")
        with kpi3:
            st.metric("Average Latency", f"{df_history['latency_seconds'].mean():.2f}s")
        with kpi4:
            st.metric("Unique Topics", df_history["topic"].nunique())
            
        st.markdown("---")
        
        # Plotly Visualizations
        chart_c1, chart_c2 = st.columns(2)
        
        with chart_c1:
            # Quality Score by Variation Type
            fig_box = px.box(
                df_history, 
                x="variation_type", 
                y="quality_score",
                color="variation_type",
                title="Quality Score Distribution by Post Variation",
                points="all"
            )
            fig_box.update_layout(template="plotly_dark")
            st.plotly_chart(fig_box, use_container_width=True)
            
        with chart_c2:
            # Latency Scatter across time
            fig_scat = px.scatter(
                df_history,
                x="timestamp",
                y="latency_seconds",
                color="variation_type",
                size="word_count",
                hover_data=["topic", "quality_score"],
                title="Inference Latency Timeline (s)"
            )
            fig_scat.update_layout(template="plotly_dark")
            st.plotly_chart(fig_scat, use_container_width=True)
            
        st.markdown("#### 📜 Persistent Database Audit Table")
        st.dataframe(
            df_history[[
                "id", "timestamp", "topic", "variation_type", "length", 
                "language", "model_name", "quality_score", "word_count", "latency_seconds"
            ]],
            use_container_width=True
        )


# ==============================================================================
# TAB 5: FEW-SHOT KNOWLEDGE BASE (SANITIZED & SAFE)
# ==============================================================================
with tab_dataset:
    st.markdown("### 📚 Few-Shot In-Context Learning Exemplar Base")
    st.markdown("""
    Few-shot in-context learning conditions LLMs by providing exemplary posts within the prompt. 
    Below is the annotated post repository parsed and sanitized safely for PyArrow compatibility.
    """)
    
    # Safe DataFrame display
    st.dataframe(fs.df[["text", "language", "line_count", "length", "tags"]], use_container_width=True)
    
    with st.expander("➕ Ingest New High-Performing Exemplar", expanded=False):
        with st.form("add_exemplar_custom"):
            new_text = st.text_area("Exemplar Post Text", placeholder="Paste proven viral LinkedIn post...")
            col_l, col_t = st.columns(2)
            with col_l:
                new_lang = st.selectbox("Language", ["English", "Hinglish"])
            with col_t:
                new_tags = st.text_input("Tags (comma separated)", placeholder="e.g. AI Ethics, Deep Learning")
            submit_btn = st.form_submit_button("Ingest into Dataset")
            if submit_btn:
                if new_text and new_tags:
                    tags_arr = [t.strip() for t in new_tags.split(",") if t.strip()]
                    fs.add_custom_post(new_text, new_lang, tags_arr)
                    st.success("Exemplar appended and sanitized! The model will utilize it in future generations.")
                else:
                    st.error("Please fill in both post content and tags.")


# ==============================================================================
# TAB 6: VIVA VOCE & TECHNICAL ARCHITECTURE DEFENSE
# ==============================================================================
with tab_defense:
    st.markdown("### 🎓 Academic Capstone Defense & Technical Architecture")
    st.caption("Prepared for External Viva Voce, Technical Evaluation, and Project Presentations.")
    
    col_arch1, col_arch2 = st.columns([1.5, 1])
    
    with col_arch1:
        st.markdown("""
        #### 🏗️ System Flow & Engineering Pipeline
        1. **User Parameters**: Topic, persona, length constraint, and language script.
        2. **Dynamic In-Context Filtering**: Searches the exemplar dataset for top-matching human posts matching language and domain metadata.
        3. **Prompt Composition**: Assembles strict structural constraints (Hooks, Pacing, CTA, Hashtags) with in-context few-shot examples.
        4. **Groq LPU Inference**: Invokes ultra-fast models (`openai/gpt-oss-120b` / `qwen/qwen3.8-27b`) delivering outputs in sub-second latency.
        5. **Quality Scorecard Analysis**: Heuristic scoring evaluating Hook impact, White-space pacing, CTA density, and Hashtags.
        6. **Persistent SQLite Persistence**: Full logging into `nexpost.db` for verifiable performance auditing.
        """)
        
    with col_arch2:
        st.markdown("""
        #### 💡 Viva Questions & Theoretical Answers
        - **Q: Why Few-Shot In-Context Prompting over Fine-Tuning?**  
          *A:* Fine-tuning requires massive annotated datasets, heavy compute budgets, and can induce catastrophic forgetting. Few-Shot In-Context Prompting adapts dynamically at runtime without altering weights.
        - **Q: How does Groq achieve sub-second generation?**  
          *A:* Groq's Tensor Streaming Processors (LPUs) eliminate GPU memory-bandwidth bottlenecks through deterministic scheduling, yielding ultra-high token throughput.
        - **Q: How was Unicode Surrogate safety resolved?**  
          *A:* Implemented automated UTF-8 surrogate sanitation routines preventing PyArrow and serialization crashes during tabular streaming.
        """)

# ==============================================================================
# GLOBAL FOOTER WITH CREATOR ATTRIBUTION
# ==============================================================================
st.markdown("""
<div class="app-footer">
    &copy; 2026 <strong>Kartikey Sabharwal</strong> &bull; NexPost AI Studio &bull; Final Year Generative AI Submission Ready
</div>
""", unsafe_allow_html=True)
