package com.djokersoft.calculadora;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.TextField;
import javafx.scene.layout.*;
import javafx.stage.Stage;
import javafx.geometry.*;

public class Calculadora extends Application {

    private TextField display = new TextField();
    private double num1 = 0;
    private String operator = "";

    @Override
    public void start(Stage stage) {
        display.setEditable(false);
        display.setMinHeight(50);
        display.setMaxWidth(Double.MAX_VALUE);
        display.setStyle("-fx-font-size: 18px;");

        GridPane grid = new GridPane();
        grid.setHgap(5);
        grid.setVgap(5);
        grid.setPadding(new Insets(10));

        for (int i = 0; i < 4; i++) {
            ColumnConstraints cc = new ColumnConstraints();
            cc.setPercentWidth(25);
            cc.setHgrow(Priority.ALWAYS);
            grid.getColumnConstraints().add(cc);
        }

        for (int i = 0; i < 4; i++) {
            RowConstraints rc = new RowConstraints();
            rc.setPercentHeight(25);
            rc.setVgrow(Priority.ALWAYS);
            grid.getRowConstraints().add(rc);
        }

        String[][] buttons = {
            {"7", "8", "9", "/"},
            {"4", "5", "6", "*"},
            {"1", "2", "3", "-"},
            {"0", "C", "=", "+"}
        };

        for (int row = 0; row < buttons.length; row++) {
            for (int col = 0; col < buttons[row].length; col++) {
                String text = buttons[row][col];
                Button btn = new Button(text);
                btn.setMaxSize(Double.MAX_VALUE, Double.MAX_VALUE);
                btn.setStyle("-fx-font-size: 16px;");
                btn.setOnAction(e -> handleButton(text));
                grid.add(btn, col, row);
                GridPane.setHgrow(btn, Priority.ALWAYS);
                GridPane.setVgrow(btn, Priority.ALWAYS);
            }
        }

        VBox root = new VBox(10, display, grid);
        root.setPadding(new Insets(10));
        VBox.setVgrow(grid, Priority.ALWAYS);

        Scene scene = new Scene(root, 300, 400);
        scene.getStylesheets().add("file:../css/style.css");

        stage.setScene(scene);
        stage.setTitle("Calculadora JavaFX");
        stage.show();
    }

    private void handleButton(String text) {
        switch (text) {
            case "C":
                display.clear();
                num1 = 0;
                operator = "";
                break;
            case "=":
                calculate();
                break;
            case "+": case "-": case "*": case "/":
                try {
                    num1 = Double.parseDouble(display.getText());
                } catch (Exception e) {
                    num1 = 0;
                }
                operator = text;
                display.clear();
                break;
            default:
                display.appendText(text);
        }
    }

    private void calculate() {
        double num2;
        try {
            num2 = Double.parseDouble(display.getText());
        } catch (Exception e) {
            display.setText("Erro");
            return;
        }

        double result = 0;
        switch (operator) {
            case "+": result = num1 + num2; break;
            case "-": result = num1 - num2; break;
            case "*": result = num1 * num2; break;
            case "/": result = num2 != 0 ? num1 / num2 : 0; break;
        }
        display.setText(String.valueOf(result));
    }

    public static void main(String[] args) {
        launch(args);
    }
}
