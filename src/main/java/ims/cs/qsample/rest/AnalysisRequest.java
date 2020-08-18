package ims.cs.qsample.rest;

public class AnalysisRequest {
    private String text;

    public AnalysisRequest(String text) {
        this.text = text;
    }

    public AnalysisRequest() {}

    public void setText(String text) {
        this.text = text;
    }

    public String getText() {
        return text;
    }
}