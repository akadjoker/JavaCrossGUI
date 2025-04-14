package org.javafxports.helloworld;

import javafx.application.Application;
import javafx.geometry.Rectangle2D;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.layout.StackPane;
import javafx.scene.paint.Color;
import javafx.scene.shape.Rectangle;
import javafx.stage.Screen;
import javafx.stage.Stage;

public class HelloAndroid extends Application {

    // Variável de instância para contar os cliques
    private int cnt = 0;
    
    @Override
    public void start(Stage stage) throws Exception {
        // Obter os limites visuais do ecrã
        Screen primaryScreen = Screen.getPrimary();
        Rectangle2D visualBounds = primaryScreen.getVisualBounds();
        double width = visualBounds.getWidth();
        double height = visualBounds.getHeight();
        
        // Cria um rótulo que mostra a mensagem e o contador de cliques
        Label label = new Label("Clique no botão. Clques: " + cnt);
        label.setTranslateY(30);
        
        // Cria um botão e define a ação de clique
        Button button = new Button("Hello Android");
        button.setOnAction(e -> {
            cnt++; // Incrementa o contador a cada clique
            label.setText("Clique no botão. Clques: " + cnt); // Atualiza o rótulo com o contador
        });
        
        // Cria um retângulo de fundo com dimensões baseadas no ecrã
        Rectangle rectangle = new Rectangle(width - 20, height - 20);
        rectangle.setFill(Color.LIGHTBLUE);
        rectangle.setArcHeight(6);
        rectangle.setArcWidth(6);
        
        // Organiza os nós em um StackPane
        StackPane stackPane = new StackPane();
        stackPane.getChildren().addAll( button, label);
        
        // Cria a cena com a dimensão total do ecrã
        Scene scene = new Scene(stackPane, width, height);
        stage.setScene(scene);
        stage.setTitle("Hello Android");
        stage.show();
    }

    
}
