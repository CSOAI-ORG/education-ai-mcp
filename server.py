"""
Education AI MCP Server
EdTech tools for teachers and educators powered by MEOK AI Labs.
"""


import sys, os
sys.path.insert(0, os.path.expanduser('~/clawd/meok-labs-engine/shared'))
from auth_middleware import check_access

import time
import random
import hashlib
from datetime import date
from collections import defaultdict
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("education-ai", instructions="MEOK AI Labs MCP Server")

_call_counts: dict[str, list[float]] = defaultdict(list)
FREE_TIER_LIMIT = 50
WINDOW = 86400


def _check_rate_limit(tool_name: str) -> None:
    now = time.time()
    _call_counts[tool_name] = [t for t in _call_counts[tool_name] if now - t < WINDOW]
    if len(_call_counts[tool_name]) >= FREE_TIER_LIMIT:
        raise ValueError(f"Rate limit exceeded for {tool_name}. Free tier: {FREE_TIER_LIMIT}/day.")
    _call_counts[tool_name].append(now)


BLOOMS_TAXONOMY = {
    "remember": ["define", "list", "identify", "name", "recall", "state", "match"],
    "understand": ["explain", "describe", "summarize", "interpret", "classify", "compare"],
    "apply": ["demonstrate", "solve", "use", "implement", "calculate", "execute"],
    "analyze": ["differentiate", "examine", "compare", "contrast", "investigate", "deconstruct"],
    "evaluate": ["judge", "critique", "assess", "justify", "defend", "argue"],
    "create": ["design", "construct", "produce", "invent", "compose", "formulate"],
}

LEARNING_STYLES = {
    "visual": {"activities": ["diagrams", "mind maps", "videos", "infographics", "color-coded notes"],
               "assessment": ["poster creation", "diagram labeling", "visual presentation"]},
    "auditory": {"activities": ["group discussion", "podcasts", "verbal explanation", "debate", "songs/mnemonics"],
                 "assessment": ["oral presentation", "recorded explanation", "group debate"]},
    "kinesthetic": {"activities": ["hands-on experiments", "role-play", "building models", "field trips", "simulations"],
                    "assessment": ["practical demonstration", "project building", "lab work"]},
    "reading_writing": {"activities": ["note-taking", "essays", "research papers", "reading assignments", "journaling"],
                        "assessment": ["written report", "essay", "research summary"]},
}


@mcp.tool()
def generate_lesson_plan(
    subject: str,
    topic: str,
    age_group: str = "14-16",
    duration_minutes: int = 60,
    learning_objectives: list[str] | None = None,
    differentiation: bool = True, api_key: str = "") -> dict:
    """Generate a structured lesson plan with objectives, activities, and assessment.

    Args:
        subject: Subject area (e.g. "Mathematics", "Science", "English")
        topic: Specific topic (e.g. "Quadratic Equations", "Photosynthesis")
        age_group: Student age range (e.g. "11-13", "14-16", "16-18")
        duration_minutes: Lesson duration in minutes
        learning_objectives: Custom objectives (auto-generated if omitted)
        differentiation: Include differentiation strategies
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    _check_rate_limit("generate_lesson_plan")

    if not learning_objectives:
        learning_objectives = [
            f"Students will be able to define and identify key concepts of {topic}",
            f"Students will be able to apply knowledge of {topic} to solve problems",
            f"Students will be able to analyze and evaluate {topic} in different contexts",
        ]

    # Time allocation
    intro_time = max(5, duration_minutes // 6)
    main_time = duration_minutes // 2
    activity_time = duration_minutes // 4
    plenary_time = duration_minutes - intro_time - main_time - activity_time

    plan = {
        "subject": subject,
        "topic": topic,
        "age_group": age_group,
        "duration": f"{duration_minutes} minutes",
        "date": date.today().isoformat(),
        "learning_objectives": learning_objectives,
        "structure": {
            "starter": {
                "duration": f"{intro_time} min",
                "activity": f"Quick recall quiz on prior knowledge related to {topic}. "
                           f"Display 3-4 key questions on the board for paired discussion.",
                "resources": ["Whiteboard/projector", "Mini whiteboards for students"],
            },
            "main_teaching": {
                "duration": f"{main_time} min",
                "activity": f"Direct instruction on {topic} with worked examples. "
                           f"Interactive Q&A throughout. Key vocabulary introduced and displayed.",
                "resources": ["Presentation slides", "Handout with key definitions", "Worked example sheet"],
                "key_vocabulary": [topic.lower(), f"{topic.lower()} terminology"],
            },
            "independent_practice": {
                "duration": f"{activity_time} min",
                "activity": f"Students work on differentiated tasks applying {topic} concepts. "
                           f"Teacher circulates for targeted support.",
                "resources": ["Differentiated worksheet (3 levels)", "Extension task cards"],
            },
            "plenary": {
                "duration": f"{plenary_time} min",
                "activity": "Exit ticket: students answer 2 key questions demonstrating understanding. "
                           "Class discussion of common misconceptions.",
                "resources": ["Exit ticket slips"],
            },
        },
        "cross_curricular_links": [
            f"Literacy: key vocabulary and written explanations",
            f"Numeracy: data interpretation and problem-solving",
        ],
        "homework": f"Complete practice questions on {topic} (differentiated by ability). Due next lesson.",
    }

    if differentiation:
        plan["differentiation"] = {
            "support": f"Scaffolded worksheet with sentence starters and worked examples. "
                      f"Paired with peer mentor. Simplified vocabulary list.",
            "core": f"Standard worksheet with increasing difficulty. "
                   f"Expected to complete independently with minimal support.",
            "extension": f"Open-ended challenge problems requiring deeper analysis of {topic}. "
                        f"Encourage students to create their own examples.",
            "sen_adaptations": "Visual aids, extra time, modified resources as per individual plans.",
        }

    return plan


@mcp.tool()
def create_quiz(
    topic: str,
    num_questions: int = 10,
    difficulty: str = "mixed",
    question_types: list[str] | None = None,
    age_group: str = "14-16",
    include_answers: bool = True, api_key: str = "") -> dict:
    """Create a quiz with various question types aligned to Bloom's taxonomy.

    Args:
        topic: Quiz topic
        num_questions: Number of questions (max 30)
        difficulty: Difficulty level: easy, medium, hard, mixed
        question_types: Types to include: multiple_choice, true_false, short_answer, fill_blank, matching
        age_group: Target age group
        include_answers: Include answer key
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    _check_rate_limit("create_quiz")

    num_questions = min(num_questions, 30)
    question_types = question_types or ["multiple_choice", "short_answer", "true_false"]

    seed = hashlib.md5(f"{topic}{num_questions}{difficulty}".encode()).hexdigest()
    rng = random.Random(seed)

    bloom_levels = list(BLOOMS_TAXONOMY.keys())
    if difficulty == "easy":
        weights = [3, 3, 2, 1, 0, 0]
    elif difficulty == "hard":
        weights = [0, 1, 1, 2, 3, 3]
    elif difficulty == "medium":
        weights = [1, 2, 3, 2, 1, 0]
    else:
        weights = [1, 2, 2, 2, 1, 1]

    questions = []
    for i in range(num_questions):
        q_type = rng.choice(question_types)
        bloom = rng.choices(bloom_levels, weights=weights, k=1)[0]
        verb = rng.choice(BLOOMS_TAXONOMY[bloom])

        q = {
            "number": i + 1,
            "type": q_type,
            "bloom_level": bloom,
            "marks": 1 if q_type in ("multiple_choice", "true_false") else 2 if q_type == "short_answer" else 1,
        }

        if q_type == "multiple_choice":
            q["question"] = f"{verb.capitalize()} the following concept related to {topic}:"
            q["options"] = {
                "A": f"First option related to {topic}",
                "B": f"Second option related to {topic}",
                "C": f"Third option related to {topic}",
                "D": f"Fourth option related to {topic}",
            }
            if include_answers:
                q["correct_answer"] = rng.choice(["A", "B", "C", "D"])
                q["explanation"] = f"This tests the student's ability to {verb} concepts in {topic}."
        elif q_type == "true_false":
            q["question"] = f"True or False: [Statement about {topic} testing ability to {verb}]"
            if include_answers:
                q["correct_answer"] = rng.choice(["True", "False"])
        elif q_type == "short_answer":
            q["question"] = f"{verb.capitalize()} the key principle of {topic} in your own words."
            if include_answers:
                q["marking_guide"] = f"Award marks for: correct use of terminology, demonstration of {bloom}-level understanding, clear explanation."
        elif q_type == "fill_blank":
            q["question"] = f"Complete: The main concept of {topic} involves _____ which allows _____."
            if include_answers:
                q["correct_answer"] = f"[Key term], [related concept]"
        elif q_type == "matching":
            q["question"] = f"Match the following terms related to {topic} with their definitions."
            q["terms"] = [f"Term {j}" for j in range(1, 5)]
            q["definitions"] = [f"Definition {j}" for j in range(1, 5)]
            if include_answers:
                q["correct_matches"] = {f"Term {j}": f"Definition {j}" for j in range(1, 5)}

        questions.append(q)

    total_marks = sum(q["marks"] for q in questions)

    return {
        "quiz_title": f"{topic} Assessment",
        "age_group": age_group,
        "difficulty": difficulty,
        "total_questions": len(questions),
        "total_marks": total_marks,
        "estimated_time": f"{num_questions * 2} minutes",
        "questions": questions,
        "grade_boundaries": {
            "distinction": f"{int(total_marks * 0.85)}+",
            "merit": f"{int(total_marks * 0.70)}-{int(total_marks * 0.84)}",
            "pass": f"{int(total_marks * 0.50)}-{int(total_marks * 0.69)}",
            "fail": f"Below {int(total_marks * 0.50)}",
        },
        "instructions": f"Answer all questions. This quiz covers {topic} at {difficulty} difficulty.",
    }


@mcp.tool()
def analyze_student_progress(
    student_name: str,
    assessments: list[dict],
    target_grade: float = 70.0, api_key: str = "") -> dict:
    """Analyze student performance trends and generate progress report.

    Args:
        student_name: Student's name
        assessments: List of dicts with keys: subject, score (0-100), date, assessment_name (optional)
        target_grade: Target grade percentage
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    _check_rate_limit("analyze_student_progress")

    if not assessments:
        return {"error": "No assessment data provided"}

    by_subject = defaultdict(list)
    for a in assessments:
        by_subject[a.get("subject", "General")].append({
            "score": float(a.get("score", 0)),
            "date": a.get("date", ""),
            "name": a.get("assessment_name", "Assessment"),
        })

    subject_analysis = {}
    for subject, scores in by_subject.items():
        sorted_scores = sorted(scores, key=lambda x: x["date"])
        score_values = [s["score"] for s in sorted_scores]
        avg = sum(score_values) / len(score_values)

        # Trend analysis
        if len(score_values) >= 3:
            recent = sum(score_values[-3:]) / 3
            earlier = sum(score_values[:3]) / min(3, len(score_values))
            trend_diff = recent - earlier
            if trend_diff > 5:
                trend = "IMPROVING"
            elif trend_diff < -5:
                trend = "DECLINING"
            else:
                trend = "STABLE"
        else:
            trend = "INSUFFICIENT_DATA"

        on_target = avg >= target_grade

        subject_analysis[subject] = {
            "average": round(avg, 1),
            "highest": max(score_values),
            "lowest": min(score_values),
            "assessment_count": len(score_values),
            "trend": trend,
            "on_target": on_target,
            "gap_to_target": round(target_grade - avg, 1) if not on_target else 0,
            "recent_scores": sorted_scores[-3:],
        }

    all_scores = [float(a.get("score", 0)) for a in assessments]
    overall_avg = sum(all_scores) / len(all_scores)

    strengths = [s for s, d in subject_analysis.items() if d["average"] >= target_grade]
    concerns = [s for s, d in subject_analysis.items() if d["average"] < target_grade - 10]

    return {
        "student_name": student_name,
        "report_date": date.today().isoformat(),
        "overall_average": round(overall_avg, 1),
        "target_grade": target_grade,
        "on_target_overall": overall_avg >= target_grade,
        "subjects": subject_analysis,
        "strengths": strengths,
        "areas_of_concern": concerns,
        "recommendations": [
            f"Focus additional support on {c}" for c in concerns
        ] + ([f"Celebrate achievement in {s}" for s in strengths[:2]] if strengths else []),
        "total_assessments": len(assessments),
    }


@mcp.tool()
def recommend_learning_path(
    subject: str,
    current_level: str = "intermediate",
    learning_style: str = "visual",
    goals: list[str] | None = None,
    available_hours_per_week: int = 5, api_key: str = "") -> dict:
    """Recommend a personalized learning path based on student profile.

    Args:
        subject: Subject area
        current_level: Current proficiency: beginner, intermediate, advanced
        learning_style: Learning style: visual, auditory, kinesthetic, reading_writing
        goals: Specific learning goals
        available_hours_per_week: Hours available for study per week
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    _check_rate_limit("recommend_learning_path")

    goals = goals or [f"Improve proficiency in {subject}"]
    style = LEARNING_STYLES.get(learning_style, LEARNING_STYLES["visual"])

    level_map = {"beginner": 1, "intermediate": 2, "advanced": 3}
    level_num = level_map.get(current_level, 2)

    weeks_needed = {1: 12, 2: 8, 3: 6}.get(level_num, 8)

    phases = []
    phase_names = {
        1: [("Foundation", 4), ("Building Blocks", 4), ("Application", 4)],
        2: [("Consolidation", 3), ("Deepening", 3), ("Mastery Prep", 2)],
        3: [("Advanced Topics", 2), ("Specialization", 2), ("Expert Practice", 2)],
    }

    for phase_name, duration in phase_names.get(level_num, phase_names[2]):
        activities = style["activities"][:3]
        phases.append({
            "name": phase_name,
            "duration_weeks": duration,
            "hours_per_week": available_hours_per_week,
            "activities": activities,
            "milestones": [f"Complete {phase_name.lower()} assessment with 70%+ score"],
            "resources": [
                f"Recommended textbook chapter on {subject} ({phase_name.lower()})",
                f"Online practice exercises",
                f"Study group session (1hr/week)",
            ],
        })

    return {
        "student_profile": {
            "subject": subject,
            "current_level": current_level,
            "learning_style": learning_style,
            "hours_per_week": available_hours_per_week,
        },
        "goals": goals,
        "total_duration_weeks": weeks_needed,
        "total_study_hours": weeks_needed * available_hours_per_week,
        "phases": phases,
        "assessment_methods": style["assessment"],
        "tips": [
            f"As a {learning_style} learner, focus on {style['activities'][0]} and {style['activities'][1]}",
            "Review material within 24 hours for better retention",
            "Practice retrieval by testing yourself regularly",
            "Take breaks every 25-30 minutes (Pomodoro technique)",
        ],
    }


@mcp.tool()
def generate_rubric(
    assignment_title: str,
    criteria: list[str] | None = None,
    levels: int = 4,
    max_score: int = 100,
    assignment_type: str = "essay", api_key: str = "") -> dict:
    """Generate an assessment rubric with detailed criteria and descriptors.

    Args:
        assignment_title: Title of the assignment
        criteria: Custom assessment criteria (auto-generated if omitted)
        levels: Number of performance levels (3-5)
        max_score: Maximum total score
        assignment_type: Type: essay, presentation, project, lab_report, portfolio
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    _check_rate_limit("generate_rubric")

    levels = max(3, min(5, levels))

    default_criteria = {
        "essay": ["Content & Knowledge", "Analysis & Critical Thinking", "Structure & Organization", "Language & Grammar", "References & Evidence"],
        "presentation": ["Content Accuracy", "Delivery & Communication", "Visual Aids", "Audience Engagement", "Time Management"],
        "project": ["Research & Planning", "Execution & Quality", "Creativity & Innovation", "Documentation", "Reflection"],
        "lab_report": ["Hypothesis & Method", "Data Collection", "Analysis & Results", "Conclusion", "Scientific Writing"],
        "portfolio": ["Range of Work", "Quality & Depth", "Reflection & Growth", "Presentation", "Self-Assessment"],
    }

    criteria = criteria or default_criteria.get(assignment_type, default_criteria["essay"])
    points_per_criterion = max_score / len(criteria)

    level_names = {
        3: ["Below Expectations", "Meets Expectations", "Exceeds Expectations"],
        4: ["Beginning", "Developing", "Proficient", "Exemplary"],
        5: ["Inadequate", "Below Average", "Satisfactory", "Good", "Outstanding"],
    }

    names = level_names.get(levels, level_names[4])
    level_percentages = [round(i / (levels - 1), 2) for i in range(levels)]

    rubric_criteria = []
    for criterion in criteria:
        criterion_levels = []
        for i, (name, pct) in enumerate(zip(names, level_percentages)):
            score = round(points_per_criterion * pct, 1)
            if pct < 0.4:
                descriptor = f"Limited evidence of {criterion.lower()}. Significant improvement needed."
            elif pct < 0.7:
                descriptor = f"Some evidence of {criterion.lower()}. Meets basic expectations with room for growth."
            elif pct < 0.9:
                descriptor = f"Clear evidence of {criterion.lower()}. Demonstrates solid understanding and skill."
            else:
                descriptor = f"Exceptional {criterion.lower()}. Demonstrates mastery and originality."

            criterion_levels.append({
                "level": name,
                "score": score,
                "descriptor": descriptor,
            })

        rubric_criteria.append({
            "criterion": criterion,
            "max_points": round(points_per_criterion, 1),
            "weight": f"{round(100 / len(criteria), 1)}%",
            "levels": criterion_levels,
        })

    return {
        "assignment_title": assignment_title,
        "assignment_type": assignment_type,
        "max_score": max_score,
        "criteria_count": len(criteria),
        "performance_levels": names,
        "criteria": rubric_criteria,
        "grade_boundaries": {
            names[-1]: f"{int(max_score * 0.85)}-{max_score}",
            names[-2]: f"{int(max_score * 0.70)}-{int(max_score * 0.84)}",
            names[1]: f"{int(max_score * 0.50)}-{int(max_score * 0.69)}",
            names[0]: f"0-{int(max_score * 0.49)}",
        },
    }


if __name__ == "__main__":
    mcp.run()
