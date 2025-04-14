package com.djokersoft.datavizdemo;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.stage.Stage;
import javafx.animation.FadeTransition;
import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.NumberAxis;
import javafx.scene.chart.XYChart;
import javafx.scene.control.Button;
import javafx.scene.control.Slider;
import javafx.scene.layout.StackPane;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.stage.Stage;
import javafx.util.Duration;


public class DataVizDemo extends Application {

    static boolean isLineChart = true;
    
    @Override
    public void start(Stage stage) {
        stage.setTitle("Demo de Visualização de Dados");

        // Eixos do gráfico
        NumberAxis xAxis = new NumberAxis();
        xAxis.setLabel("X");

        NumberAxis yAxis = new NumberAxis();
        yAxis.setLabel("Y");

        // Criar gráfico de linha
        LineChart<Number, Number> lineChart = new LineChart<>(xAxis, yAxis);
        lineChart.setTitle("Gráfico Interativo");

        XYChart.Series<Number, Number> series = new XYChart.Series<>();
        series.setName("Exemplo de Dados");

        // Dados fictícios iniciais
        for (int i = 0; i < 10; i++) {
            series.getData().add(new XYChart.Data<>(i, Math.sin(i)));
        }

        lineChart.getData().add(series);

        // Slider para controlar o valor máximo do eixo Y
        Slider ySlider = new Slider(0, 10, 5);
        ySlider.setBlockIncrement(1);
        ySlider.setMajorTickUnit(2);
        ySlider.setShowTickLabels(true);
        ySlider.setShowTickMarks(true);

        ySlider.valueProperty().addListener((observable, oldValue, newValue) -> {
            yAxis.setUpperBound(newValue.doubleValue());
        });
       
        // Botão para alternar entre gráficos de linha e barra
        Button changeChartTypeButton = new Button("Mudar para Gráfico de Barras");
        changeChartTypeButton.setOnAction(e -> 
        {
            if (isLineChart) 
            {
                isLineChart = false;
                lineChart.getData().clear();
                // Alterando para gráfico de barras
                changeChartTypeButton.setText("Mudar para Gráfico de Linha");
                createBarChart(lineChart);
            } else {
                isLineChart = true;
                lineChart.getData().clear();
                // Voltando ao gráfico de linha
                changeChartTypeButton.setText("Mudar para Gráfico de Barras");
                createLineChart(lineChart);
            }
        });

        // Layout da aplicação
        VBox vbox = new VBox(10, lineChart, ySlider, changeChartTypeButton);
        vbox.setPadding(new Insets(20));

        // Adicionando uma transição para a mudança de gráficos
        FadeTransition fadeTransition = new FadeTransition(Duration.millis(300), lineChart);
        fadeTransition.setFromValue(1.0);
        fadeTransition.setToValue(0.0);
        fadeTransition.setCycleCount(1);
        fadeTransition.setAutoReverse(true);

     

        Scene scene = new Scene(vbox, 800, 600);
        stage.setScene(scene);
        stage.show();
    }


    private void createBarChart(LineChart<Number, Number> lineChart) {
        NumberAxis xAxis = new NumberAxis();
        xAxis.setLabel("X");
        
        NumberAxis yAxis = new NumberAxis();
        yAxis.setLabel("Y");

        XYChart.Series<Number, Number> series = new XYChart.Series<>();
        series.setName("Exemplo de Dados");

        // Dados fictícios para o gráfico de barras
        for (int i = 0; i < 10; i++) {
            series.getData().add(new XYChart.Data<>(i, Math.sin(i)));
        }

        lineChart.setTitle("Gráfico de Barras");
        lineChart.getData().add(series);
    }

    // Criar gráfico de linha
    private void createLineChart(LineChart<Number, Number> lineChart) {
        NumberAxis xAxis = new NumberAxis();
        xAxis.setLabel("X");

        NumberAxis yAxis = new NumberAxis();
        yAxis.setLabel("Y");

        XYChart.Series<Number, Number> series = new XYChart.Series<>();
        series.setName("Exemplo de Dados");

        // Dados fictícios para o gráfico de linha
        for (int i = 0; i < 10; i++) {
            series.getData().add(new XYChart.Data<>(i, Math.cos(i)));
        }

        lineChart.setTitle("Gráfico de Linha");
        lineChart.getData().add(series);
    }

    public static void main(String[] args) {
        launch(args);
    }
}
