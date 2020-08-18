package ims.cs.qsample.rest;

import ims.cs.lingdata.Document;
import ims.cs.lingdata.Token;

import java.util.*;

public class AnalysisResponse {
    public List<Map<String, String>> tokens;


    public AnalysisResponse() {}

    public AnalysisResponse(Document document) {
        tokens = new ArrayList<Map<String, String>>();
        boolean inSpan = false;

        for (Token token : document.tokenList) {
            String bioLabelPred = "O";
            boolean spanStarts = token.startsPredictedContentSpan();
            boolean spanEnds = token.endsPredictedContentSpan();

            if (spanStarts) {
                inSpan = true;
                bioLabelPred = "B";
            } else if (spanEnds) {
                inSpan = false;
                bioLabelPred = "E";
            } else if (inSpan) {
                bioLabelPred = "I";
            } else if (token.isPredictedCue) {
                bioLabelPred = "C";
            }

            String text = token.originalPredText != null ? token.originalPredText : token.predText;

            Map<String, String> t = new HashMap<>();
            t.put("text", text);
            t.put("start", String.valueOf(token.predByteCount.begin));
            t.put("end", String.valueOf(token.predByteCount.end));
            t.put("label", bioLabelPred);

            tokens.add(t);

            System.out.println(String.join("\t", text, String.valueOf(token.predByteCount.begin),
                    String.valueOf(token.predByteCount.end), token.contentBIOAnnotationGold, bioLabelPred));
        }
    }

    public List<Map<String, String>> getTokens() {
        return tokens;
    }
}