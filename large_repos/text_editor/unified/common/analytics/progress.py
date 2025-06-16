from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class ProgressData(BaseModel):
    """Tracks progress towards writing/learning goals."""
    start_time: datetime = Field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    target_words: Optional[int] = None
    target_time: Optional[timedelta] = None
    current_words: int = 0
    session_duration: timedelta = Field(default_factory=timedelta)
    words_written: int = 0
    words_deleted: int = 0
    net_words: int = 0
    
    @property
    def is_active(self) -> bool:
        """Check if the progress session is currently active."""
        return self.end_time is None
    
    @property
    def completion_percentage(self) -> float:
        """Get the completion percentage for word target."""
        if not self.target_words:
            return 0.0
        return min(100.0, (self.current_words / self.target_words) * 100)
    
    @property
    def time_percentage(self) -> float:
        """Get the completion percentage for time target."""
        if not self.target_time:
            return 0.0
        return min(100.0, (self.session_duration.total_seconds() / self.target_time.total_seconds()) * 100)
    
    @property
    def words_per_minute(self) -> float:
        """Calculate words per minute for the session."""
        if self.session_duration.total_seconds() == 0:
            return 0.0
        return (self.words_written * 60) / self.session_duration.total_seconds()
    
    @property
    def estimated_completion_time(self) -> Optional[datetime]:
        """Estimate when the word target will be completed."""
        if not self.target_words or self.words_per_minute == 0:
            return None
        
        remaining_words = max(0, self.target_words - self.current_words)
        remaining_minutes = remaining_words / self.words_per_minute
        
        return datetime.now() + timedelta(minutes=remaining_minutes)


class SessionStats(BaseModel):
    """Statistics for a writing/learning session."""
    session_id: str = Field(default_factory=lambda: str(datetime.now().timestamp()))
    start_time: datetime = Field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    words_at_start: int = 0
    words_at_end: int = 0
    peak_words: int = 0
    keystrokes: int = 0
    backspaces: int = 0
    time_active: timedelta = Field(default_factory=timedelta)
    time_idle: timedelta = Field(default_factory=timedelta)
    breaks_taken: int = 0
    
    @property
    def total_duration(self) -> timedelta:
        """Get the total session duration."""
        end = self.end_time or datetime.now()
        return end - self.start_time
    
    @property
    def productivity_ratio(self) -> float:
        """Get the ratio of active time to total time."""
        total_seconds = self.total_duration.total_seconds()
        if total_seconds == 0:
            return 0.0
        return self.time_active.total_seconds() / total_seconds
    
    @property
    def net_words(self) -> int:
        """Get the net words written in this session."""
        return self.words_at_end - self.words_at_start


class ProgressTracker(BaseModel):
    """Tracks progress and maintains session history."""
    
    current_session: Optional[ProgressData] = None
    session_history: List[SessionStats] = Field(default_factory=list)
    daily_targets: Dict[str, int] = Field(default_factory=dict)  # date -> word target
    weekly_targets: Dict[str, int] = Field(default_factory=dict)  # week -> word target
    last_activity_time: datetime = Field(default_factory=datetime.now)
    idle_threshold: timedelta = timedelta(minutes=5)
    
    def start_session(self, target_words: Optional[int] = None, 
                     target_time: Optional[timedelta] = None,
                     current_word_count: int = 0) -> ProgressData:
        """Start a new progress tracking session."""
        if self.current_session and self.current_session.is_active:
            self.end_session()
        
        self.current_session = ProgressData(
            target_words=target_words,
            target_time=target_time,
            current_words=current_word_count
        )
        
        # Start a new session stats tracking
        session_stats = SessionStats(
            words_at_start=current_word_count,
            peak_words=current_word_count
        )
        self.session_history.append(session_stats)
        
        return self.current_session
    
    def update_progress(self, current_word_count: int, words_added: int = 0, 
                       words_removed: int = 0) -> None:
        """Update the current session progress."""
        if not self.current_session or not self.current_session.is_active:
            return
        
        now = datetime.now()
        
        # Update session data
        self.current_session.current_words = current_word_count
        self.current_session.words_written += words_added
        self.current_session.words_deleted += words_removed
        self.current_session.net_words = (self.current_session.words_written - 
                                         self.current_session.words_deleted)
        
        # Update session duration
        self.current_session.session_duration = now - self.current_session.start_time
        
        # Update current session stats
        if self.session_history:
            current_stats = self.session_history[-1]
            current_stats.words_at_end = current_word_count
            current_stats.peak_words = max(current_stats.peak_words, current_word_count)
            
            # Track activity
            time_since_last = now - self.last_activity_time
            if time_since_last > self.idle_threshold:
                current_stats.time_idle += time_since_last
            else:
                current_stats.time_active += time_since_last
            
            # Track keystrokes
            if words_added > 0:
                current_stats.keystrokes += words_added * 5  # Rough estimate
            if words_removed > 0:
                current_stats.backspaces += words_removed * 5  # Rough estimate
        
        self.last_activity_time = now
    
    def end_session(self) -> Optional[ProgressData]:
        """End the current session."""
        if not self.current_session or not self.current_session.is_active:
            return None
        
        self.current_session.end_time = datetime.now()
        
        # Finalize current session stats
        if self.session_history:
            current_stats = self.session_history[-1]
            current_stats.end_time = self.current_session.end_time
        
        session = self.current_session
        self.current_session = None
        return session
    
    def set_daily_target(self, date: str, target_words: int) -> None:
        """Set a daily word target."""
        self.daily_targets[date] = target_words
    
    def set_weekly_target(self, week: str, target_words: int) -> None:
        """Set a weekly word target."""
        self.weekly_targets[week] = target_words
    
    def get_daily_progress(self, date: Optional[str] = None) -> Dict:
        """Get progress for a specific day."""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # Find sessions for this date
        daily_sessions = [
            s for s in self.session_history 
            if s.start_time.strftime("%Y-%m-%d") == date
        ]
        
        total_words = sum(s.net_words for s in daily_sessions)
        total_time = sum((s.total_duration for s in daily_sessions), timedelta())
        target = self.daily_targets.get(date, 0)
        
        return {
            "date": date,
            "words_written": total_words,
            "time_spent": total_time,
            "target_words": target,
            "completion_percentage": (total_words / target * 100) if target > 0 else 0,
            "sessions": len(daily_sessions)
        }
    
    def get_weekly_progress(self, week: Optional[str] = None) -> Dict:
        """Get progress for a specific week."""
        if week is None:
            # Get current week (ISO week)
            now = datetime.now()
            year, week_num, _ = now.isocalendar()
            week = f"{year}-W{week_num:02d}"
        
        # Parse week string
        year, week_num = week.split('-W')
        year = int(year)
        week_num = int(week_num)
        
        # Find sessions for this week
        weekly_sessions = []
        for session in self.session_history:
            session_year, session_week, _ = session.start_time.isocalendar()
            if session_year == year and session_week == week_num:
                weekly_sessions.append(session)
        
        total_words = sum(s.net_words for s in weekly_sessions)
        total_time = sum((s.total_duration for s in weekly_sessions), timedelta())
        target = self.weekly_targets.get(week, 0)
        
        return {
            "week": week,
            "words_written": total_words,
            "time_spent": total_time,
            "target_words": target,
            "completion_percentage": (total_words / target * 100) if target > 0 else 0,
            "sessions": len(weekly_sessions)
        }
    
    def get_streak_data(self) -> Dict:
        """Get writing streak information."""
        if not self.session_history:
            return {"current_streak": 0, "longest_streak": 0, "last_activity": None}
        
        # Group sessions by date
        dates_with_activity = set()
        for session in self.session_history:
            if session.net_words > 0:  # Only count productive sessions
                date = session.start_time.strftime("%Y-%m-%d")
                dates_with_activity.add(date)
        
        if not dates_with_activity:
            return {"current_streak": 0, "longest_streak": 0, "last_activity": None}
        
        # Sort dates
        sorted_dates = sorted(dates_with_activity)
        
        # Calculate current streak
        current_streak = 0
        today = datetime.now().strftime("%Y-%m-%d")
        
        for i in range(len(sorted_dates) - 1, -1, -1):
            date = sorted_dates[i]
            expected_date = (datetime.now() - timedelta(days=current_streak)).strftime("%Y-%m-%d")
            
            if date == expected_date:
                current_streak += 1
            else:
                break
        
        # Calculate longest streak
        longest_streak = 1
        current_run = 1
        
        for i in range(1, len(sorted_dates)):
            prev_date = datetime.strptime(sorted_dates[i-1], "%Y-%m-%d")
            curr_date = datetime.strptime(sorted_dates[i], "%Y-%m-%d")
            
            if (curr_date - prev_date).days == 1:
                current_run += 1
                longest_streak = max(longest_streak, current_run)
            else:
                current_run = 1
        
        return {
            "current_streak": current_streak,
            "longest_streak": longest_streak,
            "last_activity": sorted_dates[-1] if sorted_dates else None
        }
    
    def get_productivity_insights(self) -> Dict:
        """Get productivity insights and recommendations."""
        if not self.session_history:
            return {"insights": [], "recommendations": []}
        
        insights = []
        recommendations = []
        
        # Calculate averages
        recent_sessions = self.session_history[-10:]  # Last 10 sessions
        avg_words_per_session = sum(s.net_words for s in recent_sessions) / len(recent_sessions)
        avg_duration = sum((s.total_duration for s in recent_sessions), timedelta()) / len(recent_sessions)
        avg_productivity = sum(s.productivity_ratio for s in recent_sessions) / len(recent_sessions)
        
        # Insights
        if avg_words_per_session > 100:
            insights.append("You're maintaining good writing productivity!")
        elif avg_words_per_session < 50:
            insights.append("Your recent sessions have been less productive.")
            recommendations.append("Try setting smaller, achievable word targets.")
        
        if avg_productivity > 0.7:
            insights.append("You maintain good focus during writing sessions.")
        elif avg_productivity < 0.5:
            insights.append("You might be getting distracted during writing sessions.")
            recommendations.append("Consider using focus techniques or shorter sessions.")
        
        if avg_duration > timedelta(hours=2):
            insights.append("Your writing sessions are quite long.")
            recommendations.append("Consider taking breaks every hour to maintain focus.")
        
        return {
            "insights": insights,
            "recommendations": recommendations,
            "avg_words_per_session": avg_words_per_session,
            "avg_session_duration": avg_duration,
            "avg_productivity": avg_productivity
        }