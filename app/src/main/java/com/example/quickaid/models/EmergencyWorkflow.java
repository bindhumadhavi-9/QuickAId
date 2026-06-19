package com.example.quickaid.models;

import java.util.ArrayList;
import java.util.List;

public class EmergencyWorkflow {
    private String id;
    private String title;
    private String icon;
    private String description;
    private int severityLevel;
    private List<String> symptoms;
    private List<String> steps;
    private List<String> dos;
    private List<String> donts;
    private List<String> warningSigns;
    private String whenToCallEmergency;

    public EmergencyWorkflow() {
        this.symptoms = new ArrayList<>();
        this.steps = new ArrayList<>();
        this.dos = new ArrayList<>();
        this.donts = new ArrayList<>();
        this.warningSigns = new ArrayList<>();
    }

    public EmergencyWorkflow(String title, String icon, String description, int severityLevel) {
        this();
        this.title = title;
        this.icon = icon;
        this.description = description;
        this.severityLevel = severityLevel;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getIcon() {
        return icon;
    }

    public void setIcon(String icon) {
        this.icon = icon;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public int getSeverityLevel() {
        return severityLevel;
    }

    public void setSeverityLevel(int severityLevel) {
        this.severityLevel = severityLevel;
    }

    public List<String> getSymptoms() {
        return symptoms;
    }

    public void setSymptoms(List<String> symptoms) {
        this.symptoms = symptoms;
    }

    public void addSymptom(String symptom) {
        this.symptoms.add(symptom);
    }

    public List<String> getSteps() {
        return steps;
    }

    public void setSteps(List<String> steps) {
        this.steps = steps;
    }

    public void addStep(String step) {
        this.steps.add(step);
    }

    public List<String> getDos() {
        return dos;
    }

    public void setDos(List<String> dos) {
        this.dos = dos;
    }

    public void addDo(String doItem) {
        this.dos.add(doItem);
    }

    public List<String> getDonts() {
        return donts;
    }

    public void setDonts(List<String> donts) {
        this.donts = donts;
    }

    public void addDont(String dontItem) {
        this.donts.add(dontItem);
    }

    public List<String> getWarningSigns() {
        return warningSigns;
    }

    public void setWarningSigns(List<String> warningSigns) {
        this.warningSigns = warningSigns;
    }

    public void addWarningSign(String warningSign) {
        this.warningSigns.add(warningSign);
    }

    public String getWhenToCallEmergency() {
        return whenToCallEmergency;
    }

    public void setWhenToCallEmergency(String whenToCallEmergency) {
        this.whenToCallEmergency = whenToCallEmergency;
    }
}
