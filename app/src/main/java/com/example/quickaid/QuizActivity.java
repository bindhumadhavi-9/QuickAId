package com.example.quickaid;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import com.example.quickaid.models.QuizQuestion;
import com.example.quickaid.utils.Constants;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

public class QuizActivity extends AppCompatActivity {

    private TextView textViewCategory;
    private TextView textViewQuestion;
    private TextView textViewProgress;
    private RadioGroup radioGroupOptions;
    private RadioButton rbOptionA, rbOptionB, rbOptionC, rbOptionD;
    private TextView textViewExplanation;
    private TextView textViewScore;
    private Button buttonNext;
    private Button buttonSubmit;
    private View resultCard;

    private List<QuizQuestion> questions;
    private int currentQuestionIndex = 0;
    private int correctAnswers = 0;
    private String currentCategory = "general";
    private boolean answeredCurrent = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_quiz);

        if (getSupportActionBar() != null) {
            getSupportActionBar().setDisplayHomeAsUpEnabled(true);
            getSupportActionBar().setTitle("Emergency Quiz");
        }

        initViews();
        loadQuestions();
        showQuestion();
    }

    private void initViews() {
        textViewCategory = findViewById(R.id.textViewCategory);
        textViewQuestion = findViewById(R.id.textViewQuestion);
        textViewProgress = findViewById(R.id.textViewProgress);
        radioGroupOptions = findViewById(R.id.radioGroupOptions);
        rbOptionA = findViewById(R.id.rbOptionA);
        rbOptionB = findViewById(R.id.rbOptionB);
        rbOptionC = findViewById(R.id.rbOptionC);
        rbOptionD = findViewById(R.id.rbOptionD);
        textViewExplanation = findViewById(R.id.textViewExplanation);
        textViewScore = findViewById(R.id.textViewScore);
        buttonNext = findViewById(R.id.btnNext);
        buttonSubmit = findViewById(R.id.btnSubmit);
        resultCard = findViewById(R.id.resultCard);

        buttonSubmit.setOnClickListener(v -> checkAnswer());
        buttonNext.setOnClickListener(v -> nextQuestion());
    }

    private void loadQuestions() {
        questions = new ArrayList<>();
        // Load built-in questions
        questions.add(new QuizQuestion("burns", "What is the first thing you should do for a minor burn?",
            "Apply ice directly", "Run cool water over it", "Apply butter or oil", "Pop any blisters",
            "option_b", "Cool water helps reduce temperature and prevents further tissue damage. Never use ice, butter, or oil as they can worsen the injury."));

        questions.add(new QuizQuestion("choking", "What is the first step when someone is choking but can still cough?",
            "Perform abdominal thrusts", "Encourage them to cough", "Give them water", "Slap their back hard",
            "option_b", "If the person can still cough, they are still able to breathe. Encourage coughing as it is the most effective way to clear the obstruction."));

        questions.add(new QuizQuestion("general", "What is the universal emergency number in India?",
            "911", "112", "999", "108",
            "option_b", "112 is the single emergency number in India for police, fire, and ambulance services."));

        questions.add(new QuizQuestion("cpr", "What is the correct ratio of chest compressions to breaths for adult CPR?",
            "15:2", "30:2", "10:1", "20:3",
            "option_b", "For adult CPR, perform 30 chest compressions followed by 2 rescue breaths. This is the standard ratio recommended by medical guidelines."));

        questions.add(new QuizQuestion("stroke", "What does F.A.S.T. stand for in stroke recognition?",
            "Face, Arms, Speech, Time", "Fast, Alert, Strong, Tall", "Force, Action, Speed, Talk", "First Aid, Safety, Treatment",
            "option_a", "F.A.S.T. helps identify stroke: Face (drooping), Arms (weakness), Speech (slurred), Time (call emergency immediately)."));

        questions.add(new QuizQuestion("bleeding", "What is the correct way to control severe bleeding?",
            "Apply direct pressure with clean cloth", "Wash with water", "Apply a tourniquet immediately", "Let it bleed to clean wound",
            "option_a", "Direct pressure with a clean cloth is the first and most effective method to control bleeding. Elevate the limb if possible."));

        questions.add(new QuizQuestion("electric_shock", "What is the first step in helping someone with an electric shock?",
            "Touch them to pull them away", "Turn off the power source", "Pour water on them", "Call emergency services first",
            "option_b", "Always turn off the power source first. Never touch the person directly as you may also get shocked."));

        questions.add(new QuizQuestion("fractures", "What should you do if you suspect a fracture?",
            "Try to straighten the bone", "Move the person immediately", "Immobilize the area and seek medical help", "Apply heat to reduce pain",
            "option_c", "Never try to straighten or move a suspected fracture. Immobilize the area to prevent further injury and seek immediate medical attention."));

        questions.add(new QuizQuestion("heart_attack", "What is a common symptom of a heart attack?",
            "Chest pain or pressure", "Stomach ache only", "Headache", "Sore throat",
            "option_a", "Chest pain, pressure, or squeezing sensation is the most common symptom of a heart attack. Pain may also radiate to the arm, jaw, or back."));

        questions.add(new QuizQuestion("snake_bite", "What should you do for a snake bite?",
            "Cut the wound and suck out venom", "Apply a tight tourniquet", "Keep the person calm and still, seek medical help", "Apply ice to the bite",
            "option_c", "Keep the victim calm and still, immobilize the bitten area, and seek immediate medical help. Do not cut, suck, or apply tourniquets."));

        Collections.shuffle(questions);
    }

    private void showQuestion() {
        if (currentQuestionIndex >= questions.size()) {
            showFinalScore();
            return;
        }

        QuizQuestion q = questions.get(currentQuestionIndex);
        textViewCategory.setText(q.getCategory().toUpperCase());
        textViewProgress.setText((currentQuestionIndex + 1) + " / " + questions.size());
        textViewQuestion.setText(q.getQuestion());

        rbOptionA.setText(q.getOptionA());
        rbOptionB.setText(q.getOptionB());
        rbOptionC.setText(q.getOptionC());
        rbOptionD.setText(q.getOptionD());

        radioGroupOptions.clearCheck();
        resultCard.setVisibility(View.GONE);
        textViewExplanation.setVisibility(View.GONE);
        buttonSubmit.setEnabled(true);
        buttonNext.setVisibility(View.GONE);
        answeredCurrent = false;

        for (int i = 0; i < radioGroupOptions.getChildCount(); i++) {
            RadioButton rb = (RadioButton) radioGroupOptions.getChildAt(i);
            rb.setTextColor(getResources().getColor(R.color.text_primary));
        }
    }

    private void checkAnswer() {
        int selectedId = radioGroupOptions.getCheckedRadioButtonId();
        if (selectedId == -1) {
            return;
        }

        answeredCurrent = true;
        QuizQuestion q = questions.get(currentQuestionIndex);
        String selectedOption = "";

        if (selectedId == R.id.rbOptionA) selectedOption = "option_a";
        else if (selectedId == R.id.rbOptionB) selectedOption = "option_b";
        else if (selectedId == R.id.rbOptionC) selectedOption = "option_c";
        else if (selectedId == R.id.rbOptionD) selectedOption = "option_d";

        boolean isCorrect = q.isCorrectAnswer(selectedOption);

        RadioButton selected = findViewById(selectedId);
        RadioButton correctRadio = null;
        switch (q.getCorrectAnswer()) {
            case "option_a": correctRadio = rbOptionA; break;
            case "option_b": correctRadio = rbOptionB; break;
            case "option_c": correctRadio = rbOptionC; break;
            case "option_d": correctRadio = rbOptionD; break;
        }

        if (isCorrect) {
            correctAnswers++;
            selected.setTextColor(getResources().getColor(R.color.safe_green));
        } else {
            selected.setTextColor(getResources().getColor(R.color.emergency_red));
            if (correctRadio != null) {
                correctRadio.setTextColor(getResources().getColor(R.color.safe_green));
            }
        }

        resultCard.setVisibility(View.VISIBLE);
        textViewExplanation.setVisibility(View.VISIBLE);
        textViewExplanation.setText((isCorrect ? "Correct! " : "Incorrect. ") + q.getExplanation());
        buttonSubmit.setEnabled(false);
        buttonNext.setVisibility(View.VISIBLE);
    }

    private void nextQuestion() {
        currentQuestionIndex++;
        showQuestion();
    }

    private void showFinalScore() {
        setContentView(R.layout.quiz_result);
        TextView scoreText = findViewById(R.id.textViewFinalScore);
        TextView percentageText = findViewById(R.id.textViewPercentage);
        TextView messageText = findViewById(R.id.textViewMessage);
        Button restartBtn = findViewById(R.id.btnRestart);

        int percentage = (int) ((correctAnswers * 100.0) / questions.size());
        scoreText.setText(correctAnswers + " / " + questions.size());
        percentageText.setText(percentage + "%");

        if (percentage >= 80) {
            messageText.setText("Excellent! You have great emergency response knowledge!");
            messageText.setTextColor(getResources().getColor(R.color.safe_green));
        } else if (percentage >= 60) {
            messageText.setText("Good job! Keep learning to improve your emergency response skills.");
            messageText.setTextColor(getResources().getColor(R.color.info_blue));
        } else {
            messageText.setText("Consider reviewing first aid procedures. Knowledge saves lives!");
            messageText.setTextColor(getResources().getColor(R.color.warning_orange));
        }

        restartBtn.setOnClickListener(v -> {
            currentQuestionIndex = 0;
            correctAnswers = 0;
            setContentView(R.layout.activity_quiz);
            initViews();
            loadQuestions();
            showQuestion();
        });
    }

    @Override
    public boolean onSupportNavigateUp() {
        onBackPressed();
        return true;
    }
}
