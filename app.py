import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import networkx as nx
from datetime import datetime, timedelta
import json

st.set_page_config(
    page_title="CareerPath Pro",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Blue & Grey Theme CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #F5F7FA 0%, #E8EDF2 100%);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E3A5F 0%, #2C5282 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: #000000 !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] h3 {
        color: #B8D4E8 !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        font-size: 11px !important;
    }
    
    /* Headers */
    h1 {
        background: linear-gradient(135deg, #2563EB 0%, #1E40AF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900 !important;
        letter-spacing: -1.5px;
    }
    
    h2, h3, h4 {
        color: #1E3A5F !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }
    
    /* All paragraph text */
    p, span, div {
        color: #1a1a1a !important;
    }
    
    /* Cards */
    .role-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
        border-radius: 16px;
        padding: 28px;
        margin: 20px 0;
        box-shadow: 0 4px 20px rgba(30, 58, 95, 0.08);
        border-left: 5px solid #3B82F6;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .role-card::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 150px;
        height: 150px;
        background: radial-gradient(circle, rgba(59, 130, 246, 0.05) 0%, transparent 70%);
        border-radius: 50%;
        transform: translate(50%, -50%);
    }
    
    .role-card:hover {
        box-shadow: 0 8px 32px rgba(30, 58, 95, 0.15);
        transform: translateY(-4px);
        border-left-color: #2563EB;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F1F5F9 100%);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 2px 12px rgba(30, 58, 95, 0.06);
        border-top: 3px solid #3B82F6;
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .metric-card:hover {
        box-shadow: 0 6px 24px rgba(30, 58, 95, 0.12);
        transform: translateY(-2px);
    }
    
    /* Skill Tags */
    .skill-tag {
        display: inline-block;
        background: linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%);
        color: #1E40AF !important;
        padding: 8px 16px;
        border-radius: 24px;
        font-size: 12px;
        margin: 6px 4px;
        font-weight: 600;
        letter-spacing: 0.3px;
        border: 1px solid #93C5FD;
        transition: all 0.2s;
    }
    
    .skill-tag:hover {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
        color: white !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    /* Mentor Cards */
    .mentor-card {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        border-left: 5px solid #60A5FA;
        box-shadow: 0 2px 12px rgba(96, 165, 250, 0.15);
        transition: all 0.3s ease;
    }
    
    .mentor-card:hover {
        box-shadow: 0 6px 24px rgba(96, 165, 250, 0.25);
        transform: translateX(4px);
    }
    
    /* Achievement Badges */
    .achievement-badge {
        display: inline-block;
        background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
        color: #0C4A6E !important;
        padding: 8px 18px;
        border-radius: 24px;
        font-size: 12px;
        font-weight: 700;
        margin: 6px 4px;
        border: 1px solid #BAE6FD;
        box-shadow: 0 2px 8px rgba(14, 165, 233, 0.15);
    }
    
    /* Timeline Badge */
    .timeline-badge {
        display: inline-block;
        background: linear-gradient(135deg, #F1F5F9 0%, #E2E8F0 100%);
        color: #1a1a1a !important;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        border: 1px solid #CBD5E1;
    }
    
    /* Priority Badges */
    .priority-high {
        background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%);
        color: #991B1B !important;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        border: 1px solid #FCA5A5;
        letter-spacing: 0.5px;
    }
    
    .priority-medium {
        background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
        color: #92400E !important;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        border: 1px solid #FCD34D;
        letter-spacing: 0.5px;
    }
    
    .priority-low {
        background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%);
        color: #065F46 !important;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        border: 1px solid #6EE7B7;
        letter-spacing: 0.5px;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 32px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 24px rgba(37, 99, 235, 0.4) !important;
    }
    
    /* Progress Bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #3B82F6 0%, #2563EB 100%);
        border-radius: 10px;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(135deg, #1E3A5F 0%, #2563EB 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
    }
    
    [data-testid="stMetricLabel"] {
        color: #1a1a1a !important;
        font-weight: 700 !important;
        font-size: 11px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    [data-testid="stMetricDelta"] {
        color: #1a1a1a !important;
    }
    
    /* Info boxes */
    .stInfo {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%) !important;
        border-left: 4px solid #3B82F6 !important;
        border-radius: 12px !important;
        padding: 16px !important;
    }
    
    .stInfo * {
        color: #1E3A5F !important;
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%) !important;
        border-left: 4px solid #10B981 !important;
        border-radius: 12px !important;
        padding: 16px !important;
    }
    
    .stSuccess * {
        color: #065F46 !important;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%) !important;
        border-left: 4px solid #F59E0B !important;
        border-radius: 12px !important;
        padding: 16px !important;
    }
    
    .stWarning * {
        color: #92400E !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: white;
        padding: 12px;
        border-radius: 16px;
        box-shadow: 0 2px 12px rgba(30, 58, 95, 0.08);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        color: #1a1a1a !important;
        font-weight: 600;
        padding: 12px 24px;
        transition: all 0.2s;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #F1F5F9;
        color: #1E3A5F !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
        color: white !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    /* Dataframes */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 16px rgba(30, 58, 95, 0.08);
        border: 1px solid #E2E8F0;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%) !important;
        border-radius: 12px !important;
        border-left: 4px solid #3B82F6 !important;
        font-weight: 600 !important;
        padding: 16px !important;
        box-shadow: 0 2px 8px rgba(30, 58, 95, 0.06) !important;
        color: #1a1a1a !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: #F1F5F9 !important;
        box-shadow: 0 4px 16px rgba(30, 58, 95, 0.12) !important;
    }
    
    /* Expander content */
    .streamlit-expanderContent {
        background: white !important;
        border-radius: 0 0 12px 12px !important;
        padding: 20px !important;
    }
    
    .streamlit-expanderContent * {
        color: #1a1a1a !important;
    }
    
    /* Markdown text */
    .stMarkdown {
        color: #1a1a1a !important;
    }
    
    .stMarkdown p {
        color: #1a1a1a !important;
    }
    
    .stMarkdown li {
        color: #1a1a1a !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #F1F5F9;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
    }
    
    /* Number indicators */
    .number-indicator {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
        color: white !important;
        width: 48px;
        height: 48px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 20px;
        box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
    }
    
    /* Readiness score display */
    .readiness-score {
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1;
    }
    
    /* Section dividers */
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #CBD5E1 50%, transparent 100%);
        margin: 32px 0;
    }
    
    /* Stat box */
    .stat-box {
        background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
        border-radius: 12px;
        padding: 20px;
        border-left: 3px solid #94A3B8;
        margin: 12px 0;
        transition: all 0.2s;
    }
    
    .stat-box:hover {
        border-left-color: #3B82F6;
        box-shadow: 0 4px 16px rgba(59, 130, 246, 0.1);
    }
    
    /* Strong text */
    strong {
        color: #1a1a1a !important;
        font-weight: 700;
    }
    
    /* List items */
    li {
        color: #1a1a1a !important;
    }
</style>
""", unsafe_allow_html=True)

# [Keep all the data definitions the same as before - CAREER_PATHS, LEARNING_RESOURCES, employees, mentors, etc.]

# Enhanced career progression data
CAREER_PATHS = {
    'Engineering': {
        'Junior Software Engineer': {
            'level': 1,
            'next_roles': ['Software Engineer'],
            'required_skills': ['Python', 'Git', 'SQL', 'REST APIs'],
            'years_experience': '0-2',
            'avg_time_to_next': '1.5-2 years',
            'salary_range': '$60k-$80k',
            'key_responsibilities': ['Write clean code', 'Fix bugs', 'Participate in code reviews', 'Learn from senior engineers']
        },
        'Software Engineer': {
            'level': 2,
            'next_roles': ['Senior Software Engineer', 'Tech Lead'],
            'required_skills': ['System Design', 'Microservices', 'CI/CD', 'Cloud (AWS/GCP)', 'Mentoring'],
            'years_experience': '2-4',
            'avg_time_to_next': '2-3 years',
            'salary_range': '$80k-$120k',
            'key_responsibilities': ['Own features end-to-end', 'Mentor juniors', 'Participate in design', 'Ensure code quality']
        },
        'Senior Software Engineer': {
            'level': 3,
            'next_roles': ['Staff Engineer', 'Engineering Manager'],
            'required_skills': ['Architecture', 'Performance Optimization', 'Technical Leadership', 'Cross-team Collaboration'],
            'years_experience': '4-7',
            'avg_time_to_next': '2-4 years',
            'salary_range': '$120k-$160k',
            'key_responsibilities': ['Design systems', 'Lead technical initiatives', 'Mentor team', 'Drive best practices']
        },
        'Tech Lead': {
            'level': 3,
            'next_roles': ['Engineering Manager', 'Staff Engineer'],
            'required_skills': ['Team Leadership', 'Project Management', 'Stakeholder Communication', 'Technical Strategy'],
            'years_experience': '5-8',
            'avg_time_to_next': '2-3 years',
            'salary_range': '$130k-$170k',
            'key_responsibilities': ['Lead engineering team', 'Manage projects', 'Technical decisions', 'Team coordination']
        },
        'Staff Engineer': {
            'level': 4,
            'next_roles': ['Principal Engineer', 'Engineering Director'],
            'required_skills': ['System Architecture', 'Technical Vision', 'Cross-org Influence', 'Strategic Planning'],
            'years_experience': '8-12',
            'avg_time_to_next': '3-5 years',
            'salary_range': '$160k-$220k',
            'key_responsibilities': ['Define architecture', 'Influence org-wide decisions', 'Technical strategy', 'Thought leadership']
        },
        'Engineering Manager': {
            'level': 4,
            'next_roles': ['Senior Engineering Manager', 'Engineering Director'],
            'required_skills': ['People Management', 'Hiring', 'Performance Management', 'Budget Planning', 'Strategic Thinking'],
            'years_experience': '7-10',
            'avg_time_to_next': '3-4 years',
            'salary_range': '$150k-$200k',
            'key_responsibilities': ['Build and lead team', 'Hiring and retention', 'Performance reviews', 'Career development']
        },
        'Principal Engineer': {
            'level': 5,
            'next_roles': ['Distinguished Engineer', 'VP of Engineering'],
            'required_skills': ['Company-wide Impact', 'Technology Strategy', 'Industry Influence', 'Executive Communication'],
            'years_experience': '12+',
            'avg_time_to_next': '4+ years',
            'salary_range': '$220k-$300k+',
            'key_responsibilities': ['Shape company technology', 'Industry thought leadership', 'Strategic initiatives', 'Technical vision']
        },
        'Engineering Director': {
            'level': 5,
            'next_roles': ['VP of Engineering', 'CTO'],
            'required_skills': ['Org Design', 'Executive Leadership', 'Business Strategy', 'Resource Allocation', 'P&L Management'],
            'years_experience': '10+',
            'avg_time_to_next': '3-5 years',
            'salary_range': '$200k-$280k',
            'key_responsibilities': ['Lead multiple teams', 'Org structure', 'Budget management', 'Strategic planning']
        }
    },
    'Product': {
        'Associate Product Manager': {
            'level': 1,
            'next_roles': ['Product Manager'],
            'required_skills': ['Requirements Gathering', 'User Research', 'Analytics', 'Roadmapping'],
            'years_experience': '0-2',
            'avg_time_to_next': '1.5-2 years',
            'salary_range': '$70k-$90k',
            'key_responsibilities': ['Support PM initiatives', 'User research', 'Data analysis', 'Feature specifications']
        },
        'Product Manager': {
            'level': 2,
            'next_roles': ['Senior Product Manager', 'Product Lead'],
            'required_skills': ['Product Strategy', 'Stakeholder Management', 'Data-Driven Decisions', 'Go-to-Market'],
            'years_experience': '2-5',
            'avg_time_to_next': '2-3 years',
            'salary_range': '$90k-$130k',
            'key_responsibilities': ['Own product roadmap', 'Prioritize features', 'Work with engineering', 'Launch products']
        },
        'Senior Product Manager': {
            'level': 3,
            'next_roles': ['Group Product Manager', 'Director of Product'],
            'required_skills': ['Vision Setting', 'Cross-functional Leadership', 'Business Strategy', 'Market Analysis'],
            'years_experience': '5-8',
            'avg_time_to_next': '2-4 years',
            'salary_range': '$130k-$170k',
            'key_responsibilities': ['Product vision', 'Strategic initiatives', 'Cross-team leadership', 'Market strategy']
        },
        'Group Product Manager': {
            'level': 4,
            'next_roles': ['Director of Product', 'VP of Product'],
            'required_skills': ['Team Management', 'Portfolio Strategy', 'Executive Communication', 'Org Building'],
            'years_experience': '8-12',
            'avg_time_to_next': '3-5 years',
            'salary_range': '$160k-$220k',
            'key_responsibilities': ['Lead PM team', 'Portfolio management', 'Strategic planning', 'Team development']
        },
        'Director of Product': {
            'level': 5,
            'next_roles': ['VP of Product', 'CPO'],
            'required_skills': ['Product Org Leadership', 'Company Strategy', 'Executive Presence', 'P&L Ownership'],
            'years_experience': '10+',
            'avg_time_to_next': '3-5 years',
            'salary_range': '$200k-$280k',
            'key_responsibilities': ['Product org strategy', 'Business outcomes', 'Executive alignment', 'Organization building']
        }
    },
    'Data': {
        'Data Analyst': {
            'level': 1,
            'next_roles': ['Senior Data Analyst', 'Data Scientist'],
            'required_skills': ['SQL', 'Python', 'Tableau/PowerBI', 'Statistics', 'Business Intelligence'],
            'years_experience': '0-2',
            'avg_time_to_next': '2-3 years',
            'salary_range': '$65k-$85k',
            'key_responsibilities': ['Data analysis', 'Create dashboards', 'Business insights', 'Report generation']
        },
        'Senior Data Analyst': {
            'level': 2,
            'next_roles': ['Lead Data Analyst', 'Data Scientist'],
            'required_skills': ['Advanced Analytics', 'A/B Testing', 'Predictive Modeling', 'Stakeholder Management'],
            'years_experience': '3-5',
            'avg_time_to_next': '2-3 years',
            'salary_range': '$90k-$120k',
            'key_responsibilities': ['Complex analysis', 'Experiment design', 'Strategic recommendations', 'Cross-team collaboration']
        },
        'Data Scientist': {
            'level': 2,
            'next_roles': ['Senior Data Scientist', 'ML Engineer'],
            'required_skills': ['Machine Learning', 'Statistical Modeling', 'Python/R', 'Feature Engineering'],
            'years_experience': '2-5',
            'avg_time_to_next': '2-3 years',
            'salary_range': '$100k-$140k',
            'key_responsibilities': ['Build ML models', 'Feature engineering', 'Model deployment', 'Data-driven solutions']
        },
        'Senior Data Scientist': {
            'level': 3,
            'next_roles': ['Staff Data Scientist', 'Data Science Manager'],
            'required_skills': ['Advanced ML', 'Research', 'Technical Leadership', 'Business Impact'],
            'years_experience': '5-8',
            'avg_time_to_next': '3-4 years',
            'salary_range': '$140k-$180k',
            'key_responsibilities': ['Lead ML projects', 'Mentorship', 'Research and innovation', 'Strategic impact']
        },
        'Staff Data Scientist': {
            'level': 4,
            'next_roles': ['Principal Data Scientist', 'Director of Data Science'],
            'required_skills': ['AI Strategy', 'Cross-org Influence', 'Research Leadership', 'Product Innovation'],
            'years_experience': '8+',
            'avg_time_to_next': '3-5 years',
            'salary_range': '$180k-$240k',
            'key_responsibilities': ['AI strategy', 'Technical vision', 'Cross-org influence', 'Innovation leadership']
        }
    }
}

# Learning resources
LEARNING_RESOURCES = {
    'Python': ['Codecademy Python Course', 'Python for Everybody (Coursera)', 'Real Python Tutorials'],
    'System Design': ['System Design Interview (Book)', 'Grokking System Design', 'ByteByteGo'],
    'Product Strategy': ['Inspired (Book)', 'Reforge Product Strategy', 'Product School'],
    'Machine Learning': ['Andrew Ng ML Course', 'Fast.ai', 'Kaggle Learn'],
    'Leadership': ['The Manager\'s Path (Book)', 'High Output Management', 'Radical Candor']
}

# Employee data with achievements
if 'employees' not in st.session_state:
    st.session_state.employees = [
        {
            'name': 'Alex Johnson',
            'current_role': 'Software Engineer',
            'department': 'Engineering',
            'years_in_role': 2.5,
            'current_skills': ['Python', 'Git', 'SQL', 'REST APIs', 'Docker', 'Microservices'],
            'desired_role': 'Senior Software Engineer',
            'career_goals': 'Technical Leadership',
            'achievements': ['Led microservices migration', 'Mentored 2 junior engineers', 'Improved API performance by 40%'],
            'projects': [
                {'name': 'Payment System Refactor', 'impact': 'High', 'date': '2024-Q4'},
                {'name': 'API Gateway Implementation', 'impact': 'Medium', 'date': '2024-Q3'}
            ]
        },
        {
            'name': 'Maria Garcia',
            'current_role': 'Product Manager',
            'department': 'Product',
            'years_in_role': 3.0,
            'current_skills': ['Product Strategy', 'Analytics', 'Roadmapping', 'Stakeholder Management'],
            'desired_role': 'Senior Product Manager',
            'career_goals': 'Product Leadership',
            'achievements': ['Launched 3 major features', 'Increased user engagement 25%', 'Led cross-functional team of 12'],
            'projects': [
                {'name': 'Mobile App Launch', 'impact': 'High', 'date': '2024-Q4'},
                {'name': 'User Onboarding Redesign', 'impact': 'High', 'date': '2024-Q2'}
            ]
        }
    ]

if 'mentors' not in st.session_state:
    st.session_state.mentors = [
        {
            'name': 'Sarah Williams',
            'role': 'Senior Software Engineer',
            'expertise': ['System Design', 'Microservices', 'Technical Leadership'],
            'mentoring_capacity': 2,
            'current_mentees': 1,
            'years_experience': 8,
            'availability': 'Weekly 1-on-1s'
        },
        {
            'name': 'David Park',
            'role': 'Engineering Manager',
            'expertise': ['People Management', 'Career Development', 'Technical Strategy'],
            'mentoring_capacity': 3,
            'current_mentees': 2,
            'years_experience': 12,
            'availability': 'Bi-weekly sessions'
        },
        {
            'name': 'Lisa Anderson',
            'role': 'Senior Product Manager',
            'expertise': ['Product Strategy', 'Go-to-Market', 'Cross-functional Leadership'],
            'mentoring_capacity': 2,
            'current_mentees': 1,
            'years_experience': 9,
            'availability': 'Monthly check-ins'
        }
    ]

if 'open_positions' not in st.session_state:
    st.session_state.open_positions = [
        {
            'title': 'Senior Software Engineer',
            'department': 'Engineering',
            'location': 'Remote',
            'posted_date': '2025-01-15',
            'required_skills': ['Architecture', 'Performance Optimization', 'Technical Leadership'],
            'description': 'Lead technical initiatives and mentor engineers'
        },
        {
            'title': 'Tech Lead',
            'department': 'Engineering',
            'location': 'Hybrid',
            'posted_date': '2025-01-10',
            'required_skills': ['Team Leadership', 'Project Management', 'Stakeholder Communication'],
            'description': 'Lead engineering team and drive technical excellence'
        }
    ]

if 'development_plans' not in st.session_state:
    st.session_state.development_plans = []

def calculate_skill_gap(current_skills, required_skills):
    """Calculate missing skills"""
    current_set = set([s.lower() for s in current_skills])
    required_set = set([s.lower() for s in required_skills])
    missing = required_set - current_set
    return list(missing)

def calculate_readiness_score(employee, target_role, department):
    """Calculate comprehensive readiness score"""
    if target_role not in CAREER_PATHS[department]:
        return 0, {}
    
    role_data = CAREER_PATHS[department][target_role]
    
    # Skills assessment (40%)
    required_skills = role_data['required_skills']
    missing_skills = calculate_skill_gap(employee['current_skills'], required_skills)
    skill_score = ((len(required_skills) - len(missing_skills)) / len(required_skills)) * 40
    
    # Experience assessment (30%)
    years_range = role_data['years_experience'].split('-')
    min_years = float(years_range[0])
    exp_score = min(30, (employee['years_in_role'] / min_years) * 30)
    
    # Achievement assessment (20%)
    achievement_score = min(20, len(employee.get('achievements', [])) * 5)
    
    # Project impact assessment (10%)
    projects = employee.get('projects', [])
    high_impact = sum(1 for p in projects if p['impact'] == 'High')
    project_score = min(10, high_impact * 5)
    
    total_score = skill_score + exp_score + achievement_score + project_score
    
    breakdown = {
        'skills': skill_score,
        'experience': exp_score,
        'achievements': achievement_score,
        'projects': project_score
    }
    
    return total_score, breakdown

def recommend_mentors(employee, mentors):
    """Match employee with suitable mentors"""
    target_role = employee['desired_role']
    department = employee['department']
    
    if department not in CAREER_PATHS or target_role not in CAREER_PATHS[department]:
        return []
    
    required_skills = CAREER_PATHS[department][target_role]['required_skills']
    
    recommendations = []
    for mentor in mentors:
        if mentor['current_mentees'] < mentor['mentoring_capacity']:
            mentor_skills = set([s.lower() for s in mentor['expertise']])
            required_set = set([s.lower() for s in required_skills])
            match_count = len(mentor_skills & required_set)
            
            if match_count > 0:
                recommendations.append({
                    'mentor': mentor,
                    'match_score': match_count,
                    'matching_skills': list(mentor_skills & required_set)
                })
    
    return sorted(recommendations, key=lambda x: x['match_score'], reverse=True)

def recommend_internal_positions(employee, open_positions):
    """Recommend internal job openings based on skills and goals"""
    recommendations = []
    
    for position in open_positions:
        if position['department'] == employee['department']:
            required_skills = position['required_skills']
            missing = calculate_skill_gap(employee['current_skills'], required_skills)
            match_percentage = ((len(required_skills) - len(missing)) / len(required_skills)) * 100
            
            if match_percentage >= 60:
                recommendations.append({
                    'position': position,
                    'match_percentage': match_percentage,
                    'missing_skills': missing
                })
    
    return sorted(recommendations, key=lambda x: x['match_percentage'], reverse=True)

def create_career_graph(department):
    """Create network graph for career paths"""
    G = nx.DiGraph()
    roles = CAREER_PATHS[department]
    
    for role, data in roles.items():
        G.add_node(role, level=data['level'])
    
    for role, data in roles.items():
        for next_role in data['next_roles']:
            if next_role in roles:
                G.add_edge(role, next_role)
    
    return G

def main():
    # Header
    st.markdown("""
    <div style='text-align: center; padding: 48px 0 24px 0; background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%); 
                border-radius: 20px; margin-bottom: 32px; box-shadow: 0 4px 20px rgba(30, 58, 95, 0.08);'>
        <div style='display: inline-block; background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%); 
                    padding: 12px 24px; border-radius: 24px; margin-bottom: 16px;'>
            <span style='font-size: 32px;'>🎯</span>
        </div>
        <h1 style='font-size: 3.5rem; margin: 16px 0; background: linear-gradient(135deg, #1E3A5F 0%, #3B82F6 100%); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900;'>
            CareerPath Pro
        </h1>
        <p style='font-size: 18px; color: #64748B; font-weight: 500; margin: 0;'>
            Your Strategic Career Development Platform
        </p>
        <div style='margin-top: 16px; display: flex; gap: 16px; justify-content: center; flex-wrap: wrap;'>
            <span style='background: #EFF6FF; color: #1E40AF; padding: 6px 16px; border-radius: 20px; 
                         font-size: 12px; font-weight: 600;'>Career Mapping</span>
            <span style='background: #EFF6FF; color: #1E40AF; padding: 6px 16px; border-radius: 20px; 
                         font-size: 12px; font-weight: 600;'>Skill Development</span>
            <span style='background: #EFF6FF; color: #1E40AF; padding: 6px 16px; border-radius: 20px; 
                         font-size: 12px; font-weight: 600;'>Mentorship Matching</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 👤 YOUR PROFILE")
        selected_employee = st.selectbox(
            "Select Employee",
            [e['name'] for e in st.session_state.employees],
            label_visibility="collapsed"
        )
        
        employee = next(e for e in st.session_state.employees if e['name'] == selected_employee)
        
        # Calculate readiness
        readiness, breakdown = calculate_readiness_score(
            employee,
            employee['desired_role'],
            employee['department']
        )
        
        # Use markdown with proper styling - NO HTML
        st.markdown("**CURRENT ROLE**")
        st.markdown(f"**{employee['current_role']}**")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("**TARGET ROLE**")
        st.markdown(f"**{employee['desired_role']}**")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("**READINESS SCORE**")
        st.markdown(f"<div style='font-size: 32px; font-weight: 900; color: #60A5FA; margin-bottom: 8px;'>{readiness:.0f}%</div>", unsafe_allow_html=True)
        
        st.progress(readiness / 100)
        
        st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
        st.markdown("### ⚡ QUICK ACTIONS")
        
        if st.button("📊 Update Skills", use_container_width=True):
            st.session_state.show_skill_update = True
        
        if st.button("🏆 Add Achievement", use_container_width=True):
            st.session_state.show_achievement_form = True
        
        if st.button("📥 Export Career Plan", use_container_width=True):
            st.session_state.export_plan = True
        
        st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)
        st.markdown("### 📈 CAREER STATS")
        
        # Use Streamlit metrics instead of HTML to ensure black text
        st.metric("TIME IN ROLE", f"{employee['years_in_role']:.1f} years")
        st.metric("SKILLS ACQUIRED", len(employee['current_skills']))
        st.metric("ACHIEVEMENTS", len(employee.get('achievements', [])))
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Dashboard", 
        "🗺️ Career Path", 
        "📋 Development Plan", 
        "💼 Internal Jobs", 
        "🤝 Find Mentor", 
        "📚 Learning Resources"
    ])
    
    with tab1:
        st.markdown("### Career Development Dashboard")
        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
        
        readiness, breakdown = calculate_readiness_score(
            employee,
            employee['desired_role'],
            employee['department']
        )
        
        # Key metrics - Use native Streamlit metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("READINESS SCORE", f"{readiness:.0f}%", help="Overall progress towards your career goal")
        
        with col2:
            st.metric("SKILLS MASTERED", len(employee['current_skills']), help="Total technical skills acquired")
        
        with col3:
            st.metric("ACHIEVEMENTS", len(employee.get('achievements', [])), help="Career milestones completed")
        
        with col4:
            st.metric("TIME IN ROLE", f"{employee['years_in_role']:.1f} yrs", help="Years of experience in current position")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Readiness breakdown
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 📊 Readiness Breakdown")
            
            breakdown_df = pd.DataFrame({
                'Category': ['Skills', 'Experience', 'Achievements', 'Projects'],
                'Current Score': [breakdown['skills'], breakdown['experience'], breakdown['achievements'], breakdown['projects']],
                'Maximum': [40, 30, 20, 10]
            })
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                name='Your Score',
                x=breakdown_df['Category'],
                y=breakdown_df['Current Score'],
                marker=dict(
                    color=['#3B82F6', '#60A5FA', '#93C5FD', '#BFDBFE'],
                    line=dict(color='#1E40AF', width=2)
                ),
                text=breakdown_df['Current Score'].apply(lambda x: f"{x:.0f}"),
                textposition='outside',
                textfont=dict(size=14, color='#1E3A5F', family='Inter', weight='bold')
            ))
            
            fig.add_trace(go.Bar(
                name='Maximum',
                x=breakdown_df['Category'],
                y=breakdown_df['Maximum'],
                marker_color='#E2E8F0',
                opacity=0.4
            ))
            
            fig.update_layout(
                height=400,
                barmode='overlay',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='#FFFFFF',
                font=dict(family='Inter', color='#1E3A5F', size=12),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='#F1F5F9'),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            st.plotly_chart(fig, use_container_width=True, key="readiness_chart")
        
        with col2:
            st.markdown("### 🎯 Score Breakdown")
            
            for category, score in breakdown.items():
                max_score = {'skills': 40, 'experience': 30, 'achievements': 20, 'projects': 10}[category]
                percentage = (score / max_score) * 100
                
                st.markdown(f"""
                <div class='stat-box'>
                    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;'>
                        <span style='font-weight: 600; color: #1E3A5F; text-transform: capitalize;'>{category}</span>
                        <span style='font-weight: 700; color: #3B82F6;'>{score:.0f}/{max_score}</span>
                    </div>
                    <div style='width: 100%; height: 8px; background: #E2E8F0; border-radius: 10px; overflow: hidden;'>
                        <div style='width: {percentage}%; height: 100%; background: linear-gradient(90deg, #3B82F6 0%, #2563EB 100%);'></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
        
        # Achievements
        st.markdown("### 🏆 Recent Achievements")
        
        achievements_html = ""
        for achievement in employee.get('achievements', []):
            achievements_html += f"<span class='achievement-badge'>✓ {achievement}</span>"
        
        if achievements_html:
            st.markdown(f"<div style='margin: 16px 0;'>{achievements_html}</div>", unsafe_allow_html=True)
        else:
            st.info("No achievements recorded yet. Add your first achievement!")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Recent projects
        st.markdown("### 💼 Recent Projects")
        projects_df = pd.DataFrame(employee.get('projects', []))
        if not projects_df.empty:
            st.dataframe(projects_df, use_container_width=True, hide_index=True)
        else:
            st.info("No projects recorded yet.")
    
    with tab2:
        st.markdown("### 🗺️ Interactive Career Path Visualization")
        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
        
        department = employee['department']
        G = create_career_graph(department)
        
        # Calculate positions
        pos = {}
        levels = {}
        for node, data in G.nodes(data=True):
            level = data['level']
            if level not in levels:
                levels[level] = []
            levels[level].append(node)
        
        for level, nodes in levels.items():
            y = 5 - level
            for i, node in enumerate(nodes):
                x = (i - len(nodes)/2) * 3
                pos[node] = (x, y)
        
        # Create edges
        edge_trace = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace.append(
                go.Scatter(
                    x=[x0, x1, None],
                    y=[y0, y1, None],
                    mode='lines',
                    line=dict(width=3, color='#CBD5E1'),
                    hoverinfo='none',
                    showlegend=False
                )
            )
        
        # Create nodes
        node_x, node_y, node_text, node_color = [], [], [], []
        
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(node)
            
            if node == employee['current_role']:
                node_color.append('#10B981')  # Green for current
            elif node == employee['desired_role']:
                node_color.append('#F59E0B')  # Orange for target
            else:
                node_color.append('#3B82F6')  # Blue for others
        
        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=node_text,
            textposition='top center',
            textfont=dict(size=11, color='#1E3A5F', family='Inter', weight='bold'),
            marker=dict(
                size=24,
                color=node_color,
                line=dict(width=3, color='white'),
                symbol='circle'
            )
        )
        
        fig = go.Figure(data=edge_trace + [node_trace])
        fig.update_layout(
            title=dict(
                text=f"<b>{department} Career Progression Path</b>",
                font=dict(size=20, color='#1E3A5F', family='Inter')
            ),
            showlegend=False,
            height=650,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='#FFFFFF',
            margin=dict(l=20, r=20, t=80, b=20)
        )
        
        # Add legend manually
        fig.add_annotation(
            text="🟢 Current Role  🟠 Target Role  🔵 Available Paths",
            xref="paper", yref="paper",
            x=0.5, y=-0.05,
            showarrow=False,
            font=dict(size=12, color='#64748B', family='Inter')
        )
        
        st.plotly_chart(fig, use_container_width=True, key="career_graph")
        
        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
        
        # Role details
        st.markdown("### 📋 Detailed Role Information")
        
        selected_role_for_details = st.selectbox(
            "Select a role to view comprehensive details",
            list(CAREER_PATHS[department].keys())
        )
        
        role_info = CAREER_PATHS[department][selected_role_for_details]
        
        # Use columns instead of HTML for better rendering
        st.markdown(f"#### {selected_role_for_details}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Level", role_info['level'])
        with col2:
            st.metric("Salary Range", role_info['salary_range'])
        with col3:
            st.metric("Time to Next", role_info['avg_time_to_next'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Required Experience:**")
            st.info(f"{role_info['years_experience']} years")
            
            st.markdown("**🎯 Required Skills:**")
            for skill in role_info['required_skills']:
                st.markdown(f"<span class='skill-tag'>{skill}</span>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("**📈 Career Progression:**")
            if role_info['next_roles']:
                for next_role in role_info['next_roles']:
                    st.success(f"→ {next_role}")
            else:
                st.info("This is a terminal role in the career path")
        
        st.markdown("**✅ Key Responsibilities:**")
        for resp in role_info['key_responsibilities']:
            st.markdown(f"• {resp}")

    with tab3:
        st.markdown("### 📋 Your Personalized Development Plan")
        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
        
        current_role_data = CAREER_PATHS[department][employee['current_role']]
        next_roles = current_role_data['next_roles']
        
        st.markdown("#### 🎯 Recommended Next Roles")
        
        for role in next_roles:
            if role in CAREER_PATHS[department]:
                role_data = CAREER_PATHS[department][role]
                missing = calculate_skill_gap(employee['current_skills'], role_data['required_skills'])
                readiness = ((len(role_data['required_skills']) - len(missing)) / 
                           len(role_data['required_skills'])) * 100
                
                readiness_color = '#10B981' if readiness >= 70 else '#F59E0B' if readiness >= 40 else '#EF4444'
                readiness_text = 'Ready' if readiness >= 70 else 'In Progress' if readiness >= 40 else 'Developing'
                
                st.markdown(f"""
                <div class='role-card'>
                    <div style='display: flex; justify-content: space-between; align-items: start;'>
                        <div style='flex: 1;'>
                            <h3 style='margin: 0 0 12px 0; color: #1E3A5F;'>{role}</h3>
                            <div style='display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 16px;'>
                                <span class='timeline-badge'>👤 {role_data['years_experience']} experience</span>
                                <span class='timeline-badge'>💰 {role_data['salary_range']}</span>
                                <span class='timeline-badge'>⏱️ {role_data['avg_time_to_next']}</span>
                            </div>
                        </div>
                        <div style='text-align: center; min-width: 120px;'>
                            <div style='font-size: 40px; font-weight: 900; color: {readiness_color}; line-height: 1;'>
                                {readiness:.0f}%
                            </div>
                            <div style='color: #64748B; font-size: 12px; font-weight: 600; margin-top: 4px;'>
                                {readiness_text}
                            </div>
                            <div style='width: 100%; height: 6px; background: #E2E8F0; border-radius: 10px; margin-top: 8px; overflow: hidden;'>
                                <div style='width: {readiness}%; height: 100%; background: {readiness_color};'></div>
                            </div>
                        </div>
                    </div>
                    <div style='margin-top: 20px; padding-top: 20px; border-top: 1px solid #E2E8F0;'>
                        <h4 style='color: #64748B; font-size: 11px; font-weight: 700; letter-spacing: 1px; margin-bottom: 12px;'>
                            REQUIRED SKILLS
                        </h4>
                        <div>
                            {' '.join([f"<span class='skill-tag'>{skill}</span>" for skill in role_data['required_skills']])}
                        </div>
                    </div>
                    {f"<div style='margin-top: 16px; padding: 12px; background: #FEF2F2; border-radius: 8px; border-left: 3px solid #EF4444;'><strong style='color: #991B1B;'>Skills to Develop:</strong> <span style='color: #DC2626;'>{', '.join(missing)}</span></div>" if missing else "<div style='margin-top: 16px; padding: 12px; background: #F0FDF4; border-radius: 8px; border-left: 3px solid #10B981;'><strong style='color: #065F46;'>✓ All required skills acquired!</strong></div>"}
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns([3, 1])
                with col2:
                    if st.button(f"Set as Goal →", key=f"set_goal_{role}", use_container_width=True):
                        employee['desired_role'] = role
                        st.success(f"✓ Career goal updated to {role}!")
                        st.rerun()
        
        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
        
        # Action plan
        st.markdown("### 🚀 Your Action Plan")
        
        if employee['desired_role'] in CAREER_PATHS[department]:
            target_data = CAREER_PATHS[department][employee['desired_role']]
            missing = calculate_skill_gap(employee['current_skills'], target_data['required_skills'])
            
            steps = []
            
            if missing:
                steps.append({
                    'title': 'Develop Missing Skills',
                    'description': f"Focus on acquiring: {', '.join(missing[:3])}{'...' if len(missing) > 3 else ''}",
                    'timeline': '3-6 months',
                    'priority': 'High',
                    'icon': '📚'
                })
            
            steps.append({
                'title': 'Build Strong Track Record',
                'description': 'Lead high-impact projects that demonstrate readiness for the next level',
                'timeline': '6-12 months',
                'priority': 'High',
                'icon': '🎯'
            })
            
            steps.append({
                'title': 'Find an Experienced Mentor',
                'description': 'Connect with someone currently in your target role for guidance and insights',
                'timeline': '1-2 months',
                'priority': 'Medium',
                'icon': '🤝'
            })
            
            steps.append({
                'title': 'Document Your Achievements',
                'description': 'Keep detailed records of impact, metrics, and accomplishments for your promotion case',
                'timeline': 'Ongoing',
                'priority': 'Medium',
                'icon': '📊'
            })
            
            for idx, step in enumerate(steps, 1):
                priority_class = f"priority-{step['priority'].lower()}"
                
                st.markdown(f"""
                <div class='role-card'>
                    <div style='display: flex; align-items: start; gap: 20px;'>
                        <div class='number-indicator'>
                            {idx}
                        </div>
                        <div style='flex: 1;'>
                            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;'>
                                <h4 style='margin: 0; color: #1E3A5F; font-size: 18px;'>
                                    {step['icon']} {step['title']}
                                </h4>
                                <span class='{priority_class}'>
                                    {step['priority'].upper()} PRIORITY
                                </span>
                            </div>
                            <p style='margin: 0 0 12px 0; color: #475569; font-size: 14px; line-height: 1.6;'>
                                {step['description']}
                            </p>
                            <span class='timeline-badge'>⏱️ Timeline: {step['timeline']}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Timeline visualization
            st.markdown("### 📅 Projected Career Timeline")
            
            current_years = employee['years_in_role']
            target_time = float(target_data['avg_time_to_next'].split('-')[0])
            
            fig = go.Figure()
            
            # Current position
            fig.add_trace(go.Scatter(
                x=[0],
                y=[1],
                mode='markers+text',
                marker=dict(size=30, color='#10B981', line=dict(width=3, color='white')),
                text=[f"<b>{employee['current_role']}</b>"],
                textposition='bottom center',
                textfont=dict(size=12, color='#1E3A5F', family='Inter', weight='bold'),
                name='Current',
                showlegend=False
            ))
            
            # Target position
            fig.add_trace(go.Scatter(
                x=[target_time],
                y=[1],
                mode='markers+text',
                marker=dict(size=30, color='#F59E0B', line=dict(width=3, color='white')),
                text=[f"<b>{employee['desired_role']}</b>"],
                textposition='bottom center',
                textfont=dict(size=12, color='#1E3A5F', family='Inter', weight='bold'),
                name='Target',
                showlegend=False
            ))
            
            # Connection line
            fig.add_trace(go.Scatter(
                x=[0, target_time],
                y=[1, 1],
                mode='lines',
                line=dict(color='#3B82F6', width=4, dash='dash'),
                showlegend=False
            ))
            
            # Milestones
            milestones = [
                (target_time * 0.25, 'Q1: Skill Development'),
                (target_time * 0.5, 'Q2-Q3: Project Leadership'),
                (target_time * 0.75, 'Q4: Mentorship & Growth'),
            ]
            
            for x, label in milestones:
                fig.add_trace(go.Scatter(
                    x=[x],
                    y=[1.05],
                    mode='markers+text',
                    marker=dict(size=10, color='#3B82F6', symbol='diamond'),
                    text=[label],
                    textposition='top center',
                    textfont=dict(size=10, color='#64748B'),
                    showlegend=False
                ))
            
            fig.update_layout(
                title=dict(
                    text=f"<b>Estimated {target_time:.0f}-{target_time+1:.0f} Year Progression Path</b>",
                    font=dict(size=16, color='#1E3A5F', family='Inter')
                ),
                xaxis=dict(
                    title="Years",
                    range=[-0.5, target_time + 1],
                    showgrid=True,
                    gridcolor='#F1F5F9'
                ),
                yaxis=dict(
                    visible=False,
                    range=[0.5, 1.5]
                ),
                height=350,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='#FFFFFF',
                font=dict(family='Inter', color='#1E3A5F')
            )
            
            st.plotly_chart(fig, use_container_width=True, key="timeline_viz")
    
    with tab4:
        st.markdown("### 💼 Internal Job Opportunities")
        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
        
        recommendations = recommend_internal_positions(employee, st.session_state.open_positions)
        
        if not recommendations:
            st.info("🔍 No matching internal positions available at this time. Check back regularly for new opportunities!")
        else:
            st.success(f"✨ Found **{len(recommendations)}** relevant opportunities matching your skills and career goals")
            
            for rec in recommendations:
                position = rec['position']
                match_pct = rec['match_percentage']
                missing = rec['missing_skills']
                
                match_color = '#10B981' if match_pct >= 80 else '#F59E0B' if match_pct >= 60 else '#EF4444'
                
                st.markdown(f"""
                <div class='role-card'>
                    <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 16px;'>
                        <div style='flex: 1;'>
                            <h3 style='margin: 0 0 12px 0; color: #1E3A5F;'>{position['title']}</h3>
                            <div style='display: flex; gap: 12px; flex-wrap: wrap;'>
                                <span class='timeline-badge'>🏢 {position['department']}</span>
                                <span class='timeline-badge'>📍 {position['location']}</span>
                                <span class='timeline-badge'>📅 Posted: {position['posted_date']}</span>
                            </div>
                        </div>
                        <div style='text-align: center; min-width: 120px;'>
                            <div style='font-size: 40px; font-weight: 900; color: {match_color}; line-height: 1;'>
                                {match_pct:.0f}%
                            </div>
                            <div style='color: #64748B; font-size: 12px; font-weight: 600; margin-top: 4px;'>
                                Match Score
                            </div>
                        </div>
                    </div>
                    
                    <p style='color: #475569; font-size: 14px; line-height: 1.6; margin: 16px 0;'>
                        {position['description']}
                    </p>
                    
                    <div style='margin-top: 16px; padding-top: 16px; border-top: 1px solid #E2E8F0;'>
                        <h4 style='color: #64748B; font-size: 11px; font-weight: 700; letter-spacing: 1px; margin-bottom: 12px;'>
                            REQUIRED SKILLS
                        </h4>
                        <div>
                            {' '.join([f"<span class='skill-tag'>{skill}</span>" for skill in position['required_skills']])}
                        </div>
                    </div>
                    
                    {f"<div style='margin-top: 16px; padding: 12px; background: #FEF2F2; border-radius: 8px; border-left: 3px solid #EF4444;'><strong style='color: #991B1B;'>Skills Gap:</strong> <span style='color: #DC2626;'>{', '.join(missing)}</span></div>" if missing else "<div style='margin-top: 16px; padding: 12px; background: #F0FDF4; border-radius: 8px; border-left: 3px solid #10B981;'><strong style='color: #065F46;'>✓ You meet all skill requirements!</strong></div>"}
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([2, 2, 1])
                with col3:
                    if st.button(f"Apply Now →", key=f"apply_{position['title']}", use_container_width=True):
                        st.success(f"✓ Application submitted for {position['title']}!")
    
    with tab5:
        st.markdown("### 🤝 Mentorship Matching")
        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
        
        recommendations = recommend_mentors(employee, st.session_state.mentors)
        
        if not recommendations:
            st.info("🔍 No mentors with matching expertise are currently available. Check back soon or reach out to HR for recommendations!")
        else:
            st.success(f"✨ Found **{len(recommendations)}** experienced mentors aligned with your career goals")
            
            for rec in recommendations:
                mentor = rec['mentor']
                available_slots = mentor['mentoring_capacity'] - mentor['current_mentees']
                match_score = rec['match_score']
                
                # Use expander instead of complex HTML
                with st.expander(f"👤 {mentor['name']} - {mentor['role']} (Match: {match_score}/{len(mentor['expertise'])} skills)"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**Role:** {mentor['role']}")
                        st.markdown(f"**Experience:** {mentor['years_experience']} years")
                        st.markdown(f"**Availability:** {mentor['availability']}")
                        st.markdown(f"**Open Slots:** {available_slots}")
                        
                        st.markdown("**Areas of Expertise:**")
                        for skill in mentor['expertise']:
                            st.markdown(f"<span class='skill-tag'>{skill}</span>", unsafe_allow_html=True)
                        
                        st.markdown("**🎯 Matching Skills:**")
                        st.info(', '.join(rec['matching_skills']))
                    
                    with col2:
                        if st.button(f"Request Mentorship", key=f"request_{mentor['name']}", use_container_width=True):
                            st.success(f"✓ Request sent to {mentor['name']}!")

    with tab6:
        st.markdown("### 📚 Personalized Learning Resources")
        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
        
        if employee['desired_role'] in CAREER_PATHS[department]:
            target_data = CAREER_PATHS[department][employee['desired_role']]
            missing = calculate_skill_gap(employee['current_skills'], target_data['required_skills'])
            
            if missing:
                st.markdown("#### 🎯 Recommended Learning Paths for Your Goals")
                
                for skill in missing:
                    if skill in LEARNING_RESOURCES:
                        with st.expander(f"📘 Learning Path: {skill}"):
                            for idx, resource in enumerate(LEARNING_RESOURCES[skill], 1):
                                st.markdown(f"{idx}. **{resource}**")
                    else:
                        with st.expander(f"📘 {skill}"):
                            st.info("Recommended learning resources coming soon. Contact your manager or L&D team for guidance.")
            else:
                st.success("🎉 Congratulations! You've acquired all the required skills for your target role. Consider expanding into adjacent areas or preparing for the next career level.")
        else:
            st.info("Set a career goal in the Development Plan tab to see personalized learning recommendations.")
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%); padding: 40px 32px; 
                border-radius: 20px; text-align: center; box-shadow: 0 4px 20px rgba(30, 58, 95, 0.08);'>
        <div style='display: inline-block; background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%); 
                    padding: 8px 16px; border-radius: 20px; margin-bottom: 16px;'>
            <span style='color: white; font-weight: 700; font-size: 14px; letter-spacing: 1px;'>CAREERPATH PRO</span>
        </div>
        <h3 style='color: #1E3A5F; font-size: 20px; font-weight: 700; margin: 16px 0 12px 0;'>
            Empowering Careers Through Data-Driven Development
        </h3>
        <p style='color: #64748B; font-size: 14px; margin: 0 0 20px 0; max-width: 600px; margin-left: auto; margin-right: auto;'>
            Transform your career trajectory with personalized insights, structured learning paths, 
            and strategic mentorship opportunities.
        </p>
        <div style='padding-top: 20px; border-top: 1px solid #E2E8F0; color: #94A3B8; font-size: 12px;'>
            © 2025 CareerPath Pro. All rights reserved. | Made with ❤️ for professional growth
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()