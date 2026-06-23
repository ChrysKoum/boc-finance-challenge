public final class GuardrailService {
    private static final String[] BLOCKED_TERMS = {
        "hack",
        "fraud",
        "scam",
        "steal",
        "money laundering"
    };

    public boolean isBlocked(String message) {
        String normalizedMessage = message.toLowerCase();

        for (String term : BLOCKED_TERMS) {
            if (normalizedMessage.contains(term)) {
                return true;
            }
        }

        return false;
    }
}
