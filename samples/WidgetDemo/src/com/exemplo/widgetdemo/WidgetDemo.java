package com.exemplo.widgetdemo;



import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.*;
import javafx.stage.Stage;

public class WidgetDemo extends Application {

    @Override
    public void start(Stage stage) {
        Label title = new Label("Demo de Widgets");

        TextField input = new TextField();
        input.setPromptText("Escreve algo...");

        Slider slider = new Slider(0, 100, 50);
        slider.setShowTickLabels(true);
        slider.setShowTickMarks(true);

        CheckBox checkBox = new CheckBox("Ativar opção");
        Label sliderLabel = new Label("Valor: 50");

        slider.valueProperty().addListener((obs, oldVal, newVal) -> {
            sliderLabel.setText("Valor: " + newVal.intValue());
        });

        ListView <String> list = new ListView<>();
        list.getItems().addAll("Item 1", "Item 2", "Item 3", "Item 4", "Item 5", "Item 6", "Item 7", "Item 8", "Item 9", "Item 10");

        Button button = new Button("Clicar");
        Label output = new Label();

        button.setOnAction(e -> {
            String text = input.getText();
            boolean checked = checkBox.isSelected();
            output.setText("Texto: " + text + " | Check: " + checked);
        });

        ComboBox<String> comboBox = new ComboBox<>();
        comboBox.getItems().addAll("Opção A", "Opção B", "Opção C");
        comboBox.setValue("Opção A");

        ToggleGroup group = new ToggleGroup();
        RadioButton radio1 = new RadioButton("Escolha 1");
        radio1.setToggleGroup(group);
        RadioButton radio2 = new RadioButton("Escolha 2");
        radio2.setToggleGroup(group);
        HBox radioBox = new HBox(10, radio1, radio2);

        ProgressBar progress = new ProgressBar(0.5);

        ColorPicker colorPicker = new ColorPicker();
        DatePicker datePicker = new DatePicker();

        ToggleButton toggle = new ToggleButton("Ligar/Desligar");

        TextArea area = new TextArea();
        area.setPromptText("Texto longo...");

        Hyperlink link = new Hyperlink("Visita o site");
        link.setOnAction(e -> System.out.println("Clicaste no link!"));
        
        VBox layout = new VBox(5, title, input, slider, sliderLabel, checkBox, button, output, comboBox, radioBox, progress, colorPicker, datePicker, toggle, area,list, link);
        layout.setPadding(new Insets(20));

        Scene scene = new Scene(layout, 400, 600);
        stage.setTitle("Widget Demo");
        stage.setScene(scene);
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}

