package com.djokersoft.saude;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.chart.*;
import javafx.scene.control.*;
import javafx.scene.layout.*;
import javafx.stage.Stage;
import javafx.geometry.*;
import javax.script.ScriptEngineManager;
import javax.script.ScriptEngine;
import javax.script.SimpleBindings;
import java.util.stream.IntStream;
public class Saude extends Application {
    private LineChart<Number, Number> chart;
    private NumberAxis xAxis;
    private NumberAxis yAxis;
    private TextField inputFormula;
    private Slider sliderMin;
    private Slider sliderMax;
    private Label errorLabel;

    @Override
    public void start(Stage stage) {
        stage.setTitle("Gráficos de Fórmulas");

        inputFormula = new TextField("Math.sin(x)");
        inputFormula.setPrefWidth(300);

        sliderMin = new Slider(-10, 0, -10);
        sliderMax = new Slider(0, 10, 10);
        sliderMin.setShowTickLabels(true);
        sliderMax.setShowTickLabels(true);

        Button drawButton = new Button("Desenhar Gráfico");
        drawButton.setOnAction(e -> drawGraph());

        errorLabel = new Label();
        errorLabel.setStyle("-fx-text-fill: red;");

        xAxis = new NumberAxis();
        yAxis = new NumberAxis();
        chart = new LineChart<>(xAxis, yAxis);
        chart.setTitle("Resultado da Fórmula");
        chart.setCreateSymbols(false);
        chart.setMinHeight(400);

        VBox controls = new VBox(10,
                new Label("Fórmula (ex: Math.sin(x)):"), inputFormula,
                new Label("Intervalo de X (mínimo e máximo):"),
                new HBox(5, new Label("Min:"), sliderMin, new Label("Max:"), sliderMax),
                drawButton,
                errorLabel
        );
        controls.setPadding(new Insets(10));

        VBox root = new VBox(10, controls, chart);
        root.setPadding(new Insets(10));

        stage.setScene(new Scene(root, 600, 600));
        stage.show();
    }

    private void drawGraph() {
        errorLabel.setText("");

        String formula = inputFormula.getText();
        double xMin = sliderMin.getValue();
        double xMax = sliderMax.getValue();

        if (xMin >= xMax) {
            errorLabel.setText("❌ O valor mínimo de X deve ser menor que o máximo.");
            return;
        }

        XYChart.Series<Number, Number> series = new XYChart.Series<>();
        series.setName(formula);

        ScriptEngine engine = new ScriptEngineManager().getEngineByName("JavaScript");
        int points = 200;
        double step = (xMax - xMin) / points;

        try {
            for (int i = 0; i <= points; i++) {
                double x = xMin + i * step;
                double y = (Double) engine.eval(formula, new SimpleBindings() {{
                    put("x", x);
                }});
                series.getData().add(new XYChart.Data<>(x, y));
            }
            chart.getData().clear();
            chart.getData().add(series);
        } catch (Exception e) {
            errorLabel.setText("⚠️ Erro na fórmula: " + e.getMessage());
        }
    }

    public static void main(String[] args) {
        launch(args);
    }
}