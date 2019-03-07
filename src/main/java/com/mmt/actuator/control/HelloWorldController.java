package com.mmt.actuator.control;

import io.micrometer.core.instrument.Metrics;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.text.SimpleDateFormat;
import java.util.Date;

@RestController
public class HelloWorldController {
    private SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");

    @GetMapping("/helloWorld")
    public String helloWorld(){
        String humanMinute = sdf.format(new Date());
        Metrics.counter("test", "day", humanMinute).increment(1);
        return "hello world";
    }
}
