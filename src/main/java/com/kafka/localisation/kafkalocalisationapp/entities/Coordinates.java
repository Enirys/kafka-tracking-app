package com.kafka.localisation.kafkalocalisationapp.entities;

import lombok.*;

import java.util.Date;

@Data @NoArgsConstructor @AllArgsConstructor @ToString
public class Coordinates {
    private double longitude;
    private double latitude;
    private Date timestamp;
}
