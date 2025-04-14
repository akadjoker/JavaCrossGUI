package com.djokersoft.simplegame;

import javafx.animation.AnimationTimer;
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.canvas.*;
import javafx.scene.input.KeyCode;
import javafx.scene.layout.Pane;
import javafx.scene.paint.Color;
import javafx.stage.Stage;

import java.util.*;

public class SimpleGame extends Application {

    double playerX = 200;
    double playerY = 380;
    double speed = 5;

    List<double[]> enemies = new ArrayList<>();
    Random rand = new Random();
    boolean left, right;

    @Override
    public void start(Stage stage) {
        Canvas canvas = new Canvas(400, 400);
        GraphicsContext gc = canvas.getGraphicsContext2D();

        Pane root = new Pane(canvas);
        Scene scene = new Scene(root);

        scene.setOnKeyPressed(e -> {
            if (e.getCode() == KeyCode.LEFT) left = true;
            if (e.getCode() == KeyCode.RIGHT) right = true;
        });

        scene.setOnKeyReleased(e -> {
            if (e.getCode() == KeyCode.LEFT) left = false;
            if (e.getCode() == KeyCode.RIGHT) right = false;
        });

        new AnimationTimer() {
            long lastSpawn = 0;

            public void handle(long now) {
                // Update
                if (left) playerX -= speed;
                if (right) playerX += speed;
                playerX = Math.max(0, Math.min(370, playerX));

                for (double[] enemy : enemies) {
                    enemy[1] += 3; // Move down
                }
                enemies.removeIf(e -> e[1] > 400);

                // Collision detection
                for (double[] enemy : enemies) {
                    if (Math.abs(playerX - enemy[0]) < 20 && Math.abs(playerY - enemy[1]) < 20) {
                        gc.setFill(Color.RED);
                        gc.fillText("Game Over", 150, 200);
                        stop();
                        return;
                    }
                }

                // Spawn
                if (now - lastSpawn > 1e9) {
                    enemies.add(new double[]{rand.nextInt(380), 0});
                    lastSpawn = now;
                }

                // Render
                gc.setFill(Color.LIGHTGRAY);
                gc.fillRect(0, 0, 400, 400);

                gc.setFill(Color.BLUE);
                gc.fillOval(playerX, playerY, 30, 30);

                gc.setFill(Color.ORANGE);
                for (double[] enemy : enemies) {
                    gc.fillRect(enemy[0], enemy[1], 20, 20);
                }
            }
        }.start();

        stage.setTitle("Mini Jogo: Evita os Quadrados");
        stage.setScene(scene);
        stage.show();
    }
}
