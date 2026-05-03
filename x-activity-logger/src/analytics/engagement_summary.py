from profile_activity_core.analytics import build_engagement_summary as _build_engagement_summary


ENGAGEMENT_TYPES = {"tweets", "replies", "reposts", "quote_posts", "likes"}


def build_engagement_summary(database):
    return _build_engagement_summary(database, ENGAGEMENT_TYPES)
