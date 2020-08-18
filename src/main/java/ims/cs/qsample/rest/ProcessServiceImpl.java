package ims.cs.qsample.rest;

import ims.cs.qsample.rest.*;

import ims.cs.qsample.run.*;

import ims.cs.util.StaticConfig;

import ims.cs.qsample.models.QuotationPerceptrons;
import ims.cs.lingdata.Document;
import ims.cs.parc.ProcessedCorpus;

import org.springframework.stereotype.Service;

import java.io.IOException;

@Service
public class ProcessServiceImpl implements ProcessService {

    QuotationPerceptrons perceptrons;

    public ProcessServiceImpl() throws Exception {
        StaticConfig.modelForTextFileMode = StaticConfig.Model.SAMPLE;
        QSample.setConsoleMode();
        
        // load common model
        QuotationPerceptrons perceptrons = Common.deserializeModels(StaticConfig.perceptronModelFile);
        this.perceptrons = perceptrons;
    }

    @Override
    public AnalysisResponse process(AnalysisRequest req) throws Exception {

        String text = req.getText();
        System.out.println(text);
        System.out.println("STARTED");
        Document result = RunPerceptronSampler.runPsPipeline(text, perceptrons);
        System.out.println("OUTPUT_START");
        ProcessedCorpus.outputPrediction(result);
        System.out.println("OUTPUT_END");

        return new AnalysisResponse(result);
    }
}