package com.mmt.actuator;


import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Launcher {
    public static void main(String[] args){
        final SpringApplication application = new SpringApplication(Launcher.class);
        application.run(args);
    }
}
