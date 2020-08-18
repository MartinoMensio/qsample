package ims.cs.qsample.rest;

import ims.cs.qsample.rest.*;

import ims.cs.qsample.run.*;

import ims.cs.util.StaticConfig;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import org.springframework.beans.factory.annotation.Autowired;

@RestController
public class ProcessController {

    @Autowired
    ProcessService processService;

    @PostMapping("/process")
    public AnalysisResponse process(@RequestBody AnalysisRequest request) throws Exception {

        return processService.process(request);

    }
}
