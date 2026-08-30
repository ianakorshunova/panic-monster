from datetime import datetime
import base64
import mimetypes
from pathlib import Path
import random

import pandas as pd
import streamlit as st

from sqlalchemy import create_engine, text

DATABASE_URL = st.secrets["NEON_DATABASE_URL"]

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

st.set_page_config(
    page_title="Panic Monster",
    page_icon="👾",
    layout="centered",
)

def load_css(file_path: str) -> None:
    with open(file_path, encoding="utf-8") as css_file:
        st.markdown(
            f"<style>{css_file.read()}</style>",
            unsafe_allow_html=True,
        )

load_css("style.css")

@st.cache_data
def get_image_data_uri(image_path: str) -> str:
    path = Path(image_path)

    image_bytes = path.read_bytes()

    mime_type, _ = mimetypes.guess_type(path.name)

    if mime_type is None:
        mime_type = "image/png"

    encoded_image = base64.b64encode(
        image_bytes
    ).decode("utf-8")

    return (
        f"data:{mime_type};base64,"
        f"{encoded_image}"
    )


def show_monster_image(
    image_path: str,
    width: int,
    alt_text: str,
) -> None:
    image_uri = get_image_data_uri(image_path)

    st.markdown(
        f"""
        <div class="monster-image-container">
            <img
                src="{image_uri}"
                alt="{alt_text}"
                style="
                    width: {width}px;
                    max-width: 100%;
                    height: auto;
                    display: block;
                "
            >
        </div>
        """,
        unsafe_allow_html=True,
    )

def check_password() -> bool:
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True
    
    _, center, _ = st.columns([1, 1.5, 1])

    with center:
        show_monster_image(
            "assets/anxiety_monster.png",
            width=120,
            alt_text="Anxiety Monster",
        )

        st.markdown(
            """
            <div class="login-card">
                <div class="login-badge">Panic Monster</div>
                <h1 class="login-title">Welcome back</h1>
                <p class="login-subtitle">
                    Enter the password to step into your tiny monster cave.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        password = st.text_input(
            "Enter password",
            type="password",
        )

        if st.button(
            "Let me in",
            width="stretch",
        ):
            if password == st.secrets["APP_PASSWORD"]:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Wrong password")

        st.caption(
            "A tiny self-help tool for grounding, journaling, and small next steps."
        )

    return False

if not check_password():
    st.stop()

monster_help = {
    "I’m panicking": {
        "monster": "Anxiety Monster",
        "monster_image": "assets/web/anxiety_monster.png",
        "message": "No heroic decisions for 20 minutes.",
        "monster_lines": [
            "Something feels wrong. I have already checked twice.",
            "I heard a suspicious noise. It was probably danger.",
            "This seems urgent. Everything seems urgent.",
            "I brought a flashlight. We should investigate everything.",
        ],
        "steps": [
            "Put both feet on the floor.",
            "Name 5 things you can see.",
            "Drink water.",
            "Open a window or wash your hands.",
            "Do not make big decisions for 20 minutes.",
        ],
        "tiny_steps": [
            "Take three slow breaths.",
            "Drink water.",
            "Wash your hands.",
            "Stand up and stretch for 10 seconds.",
            "Put the phone down for 2 minutes.",
        ],
    },
    "I’m avoiding a task": {
        "monster": "Procrastination Monster",
        "monster_image": "assets/web/procrastination_monster.png",
        "message": (
            "The monster wants you to freeze. "
            "We only need one tiny move."
        ),
        "monster_lines": [
            "We should start soon. But first, a completely unrelated tab.",
            "Preparation is important. Endless preparation is even safer.",
            "I found seventeen easier things we could do instead.",
            "Five more minutes will definitely solve this.",
        ],
        "steps": [
            "Do not think about the whole task.",
            "Open the file or tab.",
            "Choose the smallest possible action.",
            "Set a 5-minute timer.",
            "Stop after 5 minutes if needed.",
        ],
        "tiny_steps": [
            "Open the file.",
            "Write one sentence.",
            "Set a 5-minute timer.",
            "Choose the least scary button.",
            "Close LinkedIn.",
        ],
    },
    "I feel overwhelmed": {
        "monster": "Anxiety Monster",
        "monster_image": "assets/web/anxiety_monster.png",
        "message": (
            "Too many things is not the same as "
            "all things right now."
        ),
        "monster_lines": [
            "There are too many things. We should panic about all of them.",
            "I counted the problems. Then I lost count.",
            "Everything wants attention at exactly the same time.",
            "Perhaps we should solve the entire week right now.",
        ],
        "steps": [
            "Pause for 10 seconds.",
            "Pick only one problem for the next 5 minutes.",
            "Ignore the rest for now.",
            "Write down one next step.",
            "Do only that step.",
        ],
        "tiny_steps": [
            "Write down the top 3 worries.",
            "Circle just one task.",
            "Close one extra tab.",
            "Drink water.",
            "Sit down and breathe slowly once.",
        ],
    },
    "I need one tiny step": {
        "monster": "Procrastination Monster",
        "monster_image": "assets/web/procrastination_monster.png",
        "message": "Tiny step first. Existential crisis later.",
        "monster_lines": [
            "The whole task is enormous. Let us never look at it directly.",
            "One sentence sounds suspiciously achievable.",
            "We could begin badly. I dislike this plan, but it may work.",
            "A five-minute timer is hardly a commitment.",
        ],
        "steps": [
            "Do not plan the whole day.",
            "Pick one tiny action.",
            "Make it take less than 5 minutes.",
            "Do it badly if needed.",
            "Then decide what happens next.",
        ],
        "tiny_steps": [
            "Open the file.",
            "Write one sentence.",
            "Move one task into a list.",
            "Reply with one line.",
            "Stand up and get water.",
        ],
    },
    "I need to send a scary message": {
        "monster": "Fear Monster",
        "monster_image": "assets/web/fear_monster.png",
        "message": (
            "You do not need a perfect message. "
            "You need a sent message."
        ),
        "monster_lines": [
            "Perhaps the envelope can protect us from the reply.",
            "The message exists. Unfortunately, so does the Send button.",
            "I would prefer to hide behind this folder indefinitely.",
            "Maybe one sentence is less frightening than the whole message.",
        ],
        "steps": [
            "Open the chat or email.",
            "Write a draft, not a masterpiece.",
            "Keep it short.",
            "Read it once.",
            "Send it before your brain invents a new disaster.",
        ],
        "tiny_steps": [
            "Open the chat.",
            "Write: “Hi, I wanted to ask…”",
            "Paste the draft.",
            "Remove one unnecessary sentence.",
            "Press send.",
        ],
    },
    "I need aftercare": {
        "monster": "Negativity Monster",
        "monster_image": "assets/web/negativity_monster.png",
        "message": (
            "The scary moment passed. "
            "Now we help your nervous system land."
        ),
        "monster_lines": [
            "I have prepared a detailed list of everything that went wrong.",
            "Resting seems undeserved. I object.",
            "You survived, but I still have several criticisms.",
            "Apparently we are not conducting a performance review right now.",
        ],
        "steps": [
            "Notice that you survived the moment.",
            "Drink water or sit somewhere comfortable.",
            "Rate how intense it was.",
            "Write what helped, even if it was small.",
            "Be gentle with yourself for the next hour.",
        ],
        "tiny_steps": [
            "Drink water.",
            "Write one sentence about what helped.",
            "Rate the intensity from 1 to 10.",
            "Close the scary tab.",
            "Rest for 2 minutes.",
        ],
    },
}

TRIGGER_OPTIONS = [
    "Work or job search",
    "A difficult task",
    "Messages or social interaction",
    "Health",
    "Money",
    "Family",
    "News or social media",
    "Uncertainty",
    "Sleep or exhaustion",
    "Other",
]

def save_log(
    state: str,
    monster: str,
    intensity_before: int,
    tiny_step: str,
    notes: str,
    step_completed: bool = False,
    intensity_after: int | None = None,
    trigger: str = "",
    trigger_details: str = "",
    what_helped: str = "",
) -> None:
    query = text(
        """
        INSERT INTO panic_entries (
            date_time,
            state,
            monster,
            intensity_before,
            tiny_step,
            step_completed,
            intensity_after,
            trigger,
            trigger_details,
            what_helped,
            notes
        )
        VALUES (
            :date_time,
            :state,
            :monster,
            :intensity_before,
            :tiny_step,
            :step_completed,
            :intensity_after,
            :trigger,
            :trigger_details,
            :what_helped,
            :notes
        )
        """
    )

    with engine.begin() as connection:
        connection.execute(
            query,
            {
                "date_time": datetime.now(),
                "state": state,
                "monster": monster,
                "intensity_before": intensity_before,
                "tiny_step": tiny_step,
                "step_completed": step_completed,
                "intensity_after": intensity_after,
                "trigger": trigger,
                "trigger_details": trigger_details.strip(),
                "what_helped": what_helped.strip(),
                "notes": notes.strip(),
            },
        )

def load_log() -> pd.DataFrame:
    query = text(
        """
        SELECT
            date_time,
            state,
            monster,
            intensity_before,
            tiny_step,
            step_completed,
            intensity_after,
            trigger,
            trigger_details,
            what_helped,
            notes
        FROM panic_entries
        ORDER BY date_time DESC
        """
    )

    with engine.connect() as connection:
        return pd.read_sql(query, connection)

if "selected_state" not in st.session_state:
    st.session_state.selected_state = None

if "tiny_step" not in st.session_state:
    st.session_state.tiny_step = None

if "monster_line" not in st.session_state:
    st.session_state.monster_line = None

if "step_completed" not in st.session_state:
    st.session_state.step_completed = False


st.title("👾 Panic Monster")

st.subheader(
    "Your brain is being dramatic. "
    "Let’s make the monster smaller for the next 5 minutes."
)

st.write("What is happening right now?")

state = st.radio(
    "Choose the closest option:",
    list(monster_help.keys()),
    label_visibility="collapsed",
)

if st.button("Make it 5% less scary"):
    st.session_state.selected_state = state

    st.session_state.tiny_step = random.choice(
        monster_help[state]["tiny_steps"]
    )

    st.session_state.monster_line = random.choice(
        monster_help[state]["monster_lines"]
    )

    st.session_state.step_completed = False


if st.session_state.selected_state:
    selected_state = st.session_state.selected_state
    selected_help = monster_help[selected_state]

    monster_widths = {
        "Anxiety Monster": 200,
        "Procrastination Monster": 250,
        "Fear Monster": 210,
        "Negativity Monster": 210,
    }

    image_col, text_col = st.columns([1, 2])

    with image_col:
        show_monster_image(
            image_path=selected_help["monster_image"],
            width=monster_widths[selected_help["monster"]],
            alt_text=selected_help["monster"],
        )

    with text_col:
        st.write(f"You chose: **{selected_state}**")

        st.caption(
            f"Current visitor: **{selected_help['monster']}**"
        )

        st.markdown(
            f"*“{st.session_state.monster_line}”*"
        )

        st.info(selected_help["message"])

    st.write("### Try this:")

    for step in selected_help["steps"]:
        st.write(f"- {step}")

    st.write("### Tiny step for right now:")
    st.success(st.session_state.tiny_step)

    step_col, another_col = st.columns(2)

    with another_col:
        if st.button("Give me another tiny step"):
            current_steps = selected_help["tiny_steps"]

            new_step = random.choice(current_steps)

            if len(current_steps) > 1:
                while new_step == st.session_state.tiny_step:
                    new_step = random.choice(current_steps)

            st.session_state.tiny_step = new_step
            st.session_state.step_completed = False
            st.rerun()

    with step_col:
        if st.button("I did this step"):
            st.session_state.step_completed = True
            st.rerun()

    intensity = st.slider(
        "How intense does it feel right now?",
        min_value=1,
        max_value=10,
        value=5,
    )

    trigger = st.selectbox(
        "What may have triggered this?",
        options=TRIGGER_OPTIONS,
    )

    trigger_details = st.text_input(
        "Trigger details",
        placeholder="LinkedIn, CourseKit, an unanswered message...",
    )

    notes = st.text_area(
        "Notes",
        placeholder=(
            "What happened? "
            "What does the monster keep yelling?"
        ),
    )

    if st.session_state.step_completed:
        st.subheader("How do you feel now?")

        intensity_after = st.slider(
            "Intensity after the tiny step",
            min_value=1,
            max_value=10,
            value=max(1, intensity - 1),
            key="intensity_after",
        )

        what_helped = st.text_area(
            "What helped?",
            placeholder=(
                "The timer helped, the task became clearer, "
                "I stopped checking LinkedIn..."
            ),
            key="what_helped",
        )
    else:
        intensity_after = None
        what_helped = ""

    st.divider()

    st.write("### Check in with yourself")

    if st.button("Save to Panic Log"):
        save_log(
            state=selected_state,
            monster=selected_help["monster"],
            intensity_before=intensity,
            tiny_step=st.session_state.tiny_step,
            notes=notes,
            step_completed=st.session_state.step_completed,
            intensity_after=intensity_after,
            trigger=trigger,
            trigger_details=trigger_details,
            what_helped=what_helped,
        )

        st.success(
            "Saved. The monster has been documented."
        )

    st.divider()
    st.subheader("What the monsters have been doing")

    log_df = load_log()

    if log_df.empty:
        st.caption(
            "No entries yet. The monsters have submitted no paperwork."
        )
    else:
        total_entries = len(log_df)

        average_before = log_df[
            "intensity_before"
        ].mean()

        completed_df = log_df[
            log_df["step_completed"] == True
        ].copy()

        if not completed_df.empty:
            completed_df = completed_df.dropna(
                subset=["intensity_after"]
            )

        if not completed_df.empty:
            average_after = completed_df[
                "intensity_after"
            ].mean()

            completed_df["intensity_change"] = (
                completed_df["intensity_before"]
                - completed_df["intensity_after"]
            )

            average_change = completed_df[
                "intensity_change"
            ].mean()
        else:
            average_after = None
            average_change = None

        trigger_series = (
            log_df["trigger"]
            .dropna()
            .astype(str)
        )

        trigger_series = trigger_series[
            trigger_series.str.strip() != ""
        ]

        if not trigger_series.empty:
            most_common_trigger = (
                trigger_series
                .value_counts()
                .idxmax()
            )
        else:
            most_common_trigger = "Not enough data"

        monster_series = (
            log_df["monster"]
            .dropna()
            .astype(str)
        )

        if not monster_series.empty:
            most_common_monster = (
                monster_series
                .value_counts()
                .idxmax()
            )
        else:
            most_common_monster = "Not enough data"

        most_common_monster_short = (
            most_common_monster
            .replace(" Monster", "")
        )

        metric_col_1, metric_col_2, metric_col_3 = st.columns(3)

        with metric_col_1:
            st.metric(
                "Monster visits",
                total_entries,
            )

        with metric_col_2:
            st.metric(
                "Before the tiny step",
                f"{average_before:.1f}",
            )

        with metric_col_3:
            if average_after is not None:
                st.metric(
                    "After the tiny step",
                    f"{average_after:.1f}",
                )
            else:
                st.metric(
                    "After the tiny step",
                    "No data yet",
                )

        metric_col_4, metric_col_5, metric_col_6 = st.columns(3)

        with metric_col_4:
            if average_change is not None:
                st.metric(
                    "Average change",
                    f"{average_change:.1f}",
                )
            else:
                st.metric(
                    "Average change",
                    "No data yet",
                )

        with metric_col_5:
            st.metric(
                "Loudest trigger",
                most_common_trigger,
            )

        with metric_col_6:
            st.metric(
                "Most frequent monster",
                most_common_monster_short,
            )

        st.markdown("### Recent monster visits")

        recent_columns = [
            "date_time",
            "state",
            "intensity_before",
            "step_completed",
            "intensity_after",
            "trigger",
        ]

        available_columns = [
            column
            for column in recent_columns
            if column in log_df.columns
        ]

        st.dataframe(
            log_df[available_columns]
            .tail(5)
            .sort_index(ascending=False),
            width="stretch",
            hide_index=True,
        )

        csv_data = log_df.to_csv(
            index=False,
        ).encode("utf-8-sig")

        st.download_button(
            label="Download my monster log",
            data=csv_data,
            file_name="panic_monster_log.csv",
            mime="text/csv",
        )

st.divider()

st.caption(
    "Panic Monster is a small self-help tool for grounding, "
    "journaling, and choosing tiny next steps. It does not "
    "replace professional mental health or medical support."
)