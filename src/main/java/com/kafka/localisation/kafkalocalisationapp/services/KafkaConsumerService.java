package com.kafka.localisation.kafkalocalisationapp.services;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.messaging.handler.annotation.Payload;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Service;

@Service
public class KafkaConsumerService{

    @Autowired
    SimpMessagingTemplate template;

    @KafkaListener(topics="${kafka.topic}")
    public void consume(@Payload String message) {
        template.convertAndSend("/topic/driver-coordinates", message);
    }
}
