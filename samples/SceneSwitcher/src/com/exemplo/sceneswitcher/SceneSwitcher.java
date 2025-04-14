package com.exemplo.sceneswitcher;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.TextField;
import javafx.animation.FadeTransition;
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.layout.StackPane;
import javafx.scene.layout.VBox;
import javafx.scene.text.Text;
import javafx.stage.Stage;
import javafx.util.Duration;

public class SceneSwitcher extends Application {

    private Stage stage;
    private Scene scene;
    private StackPane root;

    @Override
    public void start(Stage primaryStage) {
        this.stage = primaryStage;
        this.root = new StackPane();
        this.scene = new Scene(root, 400, 300);

        showScene1();

        primaryStage.setScene(scene);
        primaryStage.setTitle("Scene Transition Demo");
        primaryStage.show();
    }

    private void fadeTo(StackPane newContent) {
        FadeTransition fadeOut = new FadeTransition(Duration.millis(300), root);
        fadeOut.setFromValue(1.0);
        fadeOut.setToValue(0.0);
        fadeOut.setOnFinished(e -> {
            root.getChildren().setAll(newContent);
            FadeTransition fadeIn = new FadeTransition(Duration.millis(300), root);
            fadeIn.setFromValue(0.0);
            fadeIn.setToValue(1.0);
            fadeIn.play();
        });
        fadeOut.play();
    }

    private void showScene1() {
        VBox layout = new VBox(10);
        layout.setStyle("-fx-alignment: center;");
        Text text = new Text("Scene 1");
        Button button = new Button("Go to Scene 2");
        button.setOnAction(e -> showScene2());
        layout.getChildren().addAll(text, button);

        fadeTo(new StackPane(layout));
    }

    private void showScene2() {
        VBox layout = new VBox(10);
        layout.setStyle("-fx-alignment: center;");
        Text text = new Text("Scene 2");
        Button button = new Button("Go to Scene 3");
        button.setOnAction(e -> showScene3());
        layout.getChildren().addAll(text, button);

        fadeTo(new StackPane(layout));
    }

    private void showScene3() {
        VBox layout = new VBox(10);
        layout.setStyle("-fx-alignment: center;");
        Text text = new Text("Scene 3");
        Button button = new Button("Back to Scene 1");
        button.setOnAction(e -> showScene1());
        layout.getChildren().addAll(text, button);

        fadeTo(new StackPane(layout));
    }

    public static void main(String[] args) {
        launch(args);
    }
}