"""Streamlit Dashboard for AI Test Analysis."""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
from pathlib import Path

# Configure page
st.set_page_config(
    page_title="AI Test Analysis Dashboard",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    .failure-card {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    .success-card {
        background-color: #e8f5e9;
        border-left: 4px solid #4caf50;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize services
@st.cache_resource
def load_services():
    """Load the analysis services."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from src.analysis_service import AnalysisService
    from src.log_parser import LogParser
    from config import settings
    return AnalysisService(), LogParser(settings.LOGS_PATH), settings

service, parser, settings = load_services()

def load_logs():
    """Load and parse test logs."""
    if not settings.LOGS_PATH.exists():
        return [], pd.DataFrame()

    events = list(parser.parse_all())
    if not events:
        return [], pd.DataFrame()

    # Convert to DataFrame
    data = []
    for e in events:
        data.append({
            "timestamp": e.timestamp,
            "test_name": e.test_name,
            "class_name": e.class_name,
            "status": e.status,
            "message": e.message,
            "duration_ms": e.duration_ms,
            "suite": e.suite,
            "stacktrace": e.stacktrace or ""
        })
    
    df = pd.DataFrame(data)
    if not df.empty and 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    return events, df

# Load data
events, df = load_logs()

# Sidebar
st.sidebar.title("🔬 AI Test Analysis")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["📊 Dashboard", "📋 Test Events", "🔴 Failures", "🔍 Similar Search", "📈 Analytics"]
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Log File:** `{settings.LOGS_PATH}`")
st.sidebar.markdown(f"**Total Events:** {len(events)}")

if st.sidebar.button("🔄 Refresh Data"):
    st.cache_resource.clear()
    st.rerun()

st.sidebar.markdown("---")
if st.sidebar.button("📄 Generate HTML Report"):
    from report_generator import generate_html_report
    report_path = generate_html_report("test_report.html")
    st.sidebar.success(f"Report generated!")
    st.sidebar.markdown(f"[Open Report](file://{report_path})")

# Main content
if page == "📊 Dashboard":
    st.title("📊 Test Analysis Dashboard")
    
    if df.empty:
        st.warning("No test data found. Run tests first to generate logs.")
        st.code("./mvnw clean test", language="bash")
    else:
        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        total_tests = len(df[df['status'].isin(['PASSED', 'FAILED'])])
        passed = len(df[df['status'] == 'PASSED'])
        failed = len(df[df['status'] == 'FAILED'])
        pass_rate = (passed / total_tests * 100) if total_tests > 0 else 0
        
        with col1:
            st.metric("Total Tests", total_tests)
        with col2:
            st.metric("Passed", passed, delta=None)
        with col3:
            st.metric("Failed", failed, delta=None, delta_color="inverse")
        with col4:
            st.metric("Pass Rate", f"{pass_rate:.1f}%")
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Test Results Distribution")
            status_counts = df[df['status'].isin(['PASSED', 'FAILED'])]['status'].value_counts()
            fig = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                color=status_counts.index,
                color_discrete_map={'PASSED': '#4caf50', 'FAILED': '#f44336'},
                hole=0.4
            )
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Test Duration (ms)")
            duration_df = df[df['duration_ms'] > 0][['test_name', 'duration_ms']]
            if not duration_df.empty:
                fig = px.bar(
                    duration_df,
                    x='test_name',
                    y='duration_ms',
                    color='duration_ms',
                    color_continuous_scale='RdYlGn_r'
                )
                fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No duration data available")
        
        # Recent failures
        st.subheader("🔴 Recent Failures")
        failures = df[df['status'] == 'FAILED']
        if not failures.empty:
            for _, row in failures.iterrows():
                with st.expander(f"❌ {row['test_name']}", expanded=True):
                    st.markdown(f"**Class:** `{row['class_name']}`")
                    st.markdown(f"**Message:** {row['message'][:200]}...")
                    if row['stacktrace']:
                        st.code(row['stacktrace'][:500], language="java")
        else:
            st.success("✅ No failures! All tests passed.")

elif page == "📋 Test Events":
    st.title("📋 All Test Events")

    if df.empty:
        st.warning("No test data found.")
    else:
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            status_filter = st.multiselect(
                "Filter by Status",
                options=df['status'].unique().tolist(),
                default=df['status'].unique().tolist()
            )
        with col2:
            test_filter = st.multiselect(
                "Filter by Test",
                options=df['test_name'].unique().tolist(),
                default=df['test_name'].unique().tolist()
            )

        filtered_df = df[
            (df['status'].isin(status_filter)) &
            (df['test_name'].isin(test_filter))
        ]

        st.dataframe(
            filtered_df[['timestamp', 'test_name', 'status', 'message', 'duration_ms']],
            use_container_width=True,
            height=500
        )

        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="test_events.csv",
            mime="text/csv"
        )

elif page == "🔴 Failures":
    st.title("🔴 Failure Analysis")

    failures = df[df['status'] == 'FAILED']

    if failures.empty:
        st.success("✅ No failures found!")
    else:
        st.metric("Total Failures", len(failures))
        st.markdown("---")

        for idx, row in failures.iterrows():
            st.markdown(f"""
            <div class="failure-card">
                <h4>❌ {row['test_name']}</h4>
                <p><strong>Class:</strong> <code>{row['class_name']}</code></p>
                <p><strong>Time:</strong> {row['timestamp']}</p>
                <p><strong>Duration:</strong> {row['duration_ms']}ms</p>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("View Error Message"):
                st.error(row['message'])

            with st.expander("View Stacktrace"):
                if row['stacktrace']:
                    st.code(row['stacktrace'], language="java")
                else:
                    st.info("No stacktrace available")

            st.markdown("---")

elif page == "🔍 Similar Search":
    st.title("🔍 Find Similar Failures")
    st.markdown("Search for similar past failures using AI embeddings.")

    # Index data first
    if not service._indexed:
        with st.spinner("Indexing test data..."):
            service.load_and_index()

    query = st.text_area(
        "Enter error message or description:",
        placeholder="e.g., AssertionError: expected title to be...",
        height=100
    )

    top_k = st.slider("Number of results", 1, 10, 5)

    if st.button("🔍 Search", type="primary"):
        if query:
            with st.spinner("Searching..."):
                results = service.find_similar_failures(query, top_k=top_k)

            if results:
                st.success(f"Found {len(results)} similar failures")
                for i, r in enumerate(results, 1):
                    similarity = r['score'] * 100
                    color = "🟢" if similarity > 80 else "🟡" if similarity > 50 else "🔴"

                    with st.expander(f"{color} {r['test_name']} ({similarity:.1f}% similar)"):
                        st.markdown(f"**Class:** `{r['class_name']}`")
                        st.markdown(f"**Message:** {r['message'][:300]}...")
                        st.markdown(f"**Timestamp:** {r['timestamp']}")
            else:
                st.info("No similar failures found.")
        else:
            st.warning("Please enter a search query.")

elif page == "📈 Analytics":
    st.title("📈 Test Analytics")

    if df.empty:
        st.warning("No data available for analytics.")
    else:
        # Test execution timeline
        st.subheader("Test Execution Timeline")
        timeline_df = df[df['status'].isin(['PASSED', 'FAILED'])].copy()
        if not timeline_df.empty:
            fig = px.scatter(
                timeline_df,
                x='timestamp',
                y='test_name',
                color='status',
                color_discrete_map={'PASSED': '#4caf50', 'FAILED': '#f44336'},
                size='duration_ms',
                hover_data=['message']
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        # Failures by class
        st.subheader("Failures by Class")
        failures_by_class = df[df['status'] == 'FAILED']['class_name'].value_counts()
        if not failures_by_class.empty:
            fig = px.bar(
                x=failures_by_class.index,
                y=failures_by_class.values,
                labels={'x': 'Class', 'y': 'Failures'},
                color=failures_by_class.values,
                color_continuous_scale='Reds'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("No failures by class!")

        # Test duration statistics
        st.subheader("Duration Statistics")
        duration_stats = df[df['duration_ms'] > 0]['duration_ms'].describe()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Avg Duration", f"{duration_stats['mean']:.0f}ms")
        with col2:
            st.metric("Max Duration", f"{duration_stats['max']:.0f}ms")
        with col3:
            st.metric("Min Duration", f"{duration_stats['min']:.0f}ms")

        # Raw JSON viewer
        st.subheader("Raw Log Data")
        if st.checkbox("Show raw JSON"):
            for event in events[:5]:
                st.json({
                    "test_name": event.test_name,
                    "status": event.status,
                    "message": event.message,
                    "duration_ms": event.duration_ms
                })


