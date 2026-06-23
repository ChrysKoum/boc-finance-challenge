public final class MessageProcessor {
    private final GuardrailService guardrailService;

    public MessageProcessor(GuardrailService guardrailService) {
        this.guardrailService = guardrailService;
    }

    public void process(String message) throws InterruptedException {
        if (guardrailService.isBlocked(message)) {
            System.out.printf("Blocked message: \"%s\"%n", message);
            return;
        }

        System.out.printf("Processing message: \"%s\"%n", message);
        Thread.sleep(500);
        System.out.println("Processed successfully");
    }
}
