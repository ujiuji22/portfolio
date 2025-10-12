# 🐶 猫 vs 犬 画像分類器 (CNNベース)

このプロジェクトは、畳み込みニューラルネットワーク（CNN）を用いて、画像が「猫」か「犬」かを分類する二値分類モデルです。

## 🚀 デモを試す

本モデルの分類性能は、以下のWebアプリケーションからお試しいただけます。

**[Webデモはこちら (Streamlit Cloud)](https://your-streamlit-app-url.streamlit.app)**

---

## 📊 モデル学習結果の分析

学習の経過とモデルの汎用性を示すため、精度（Accuracy）と損失（Loss）の推移をプロットしました。

![精度と損失の推移グラフ](images/accuracy_loss_plot.png)

*【考察】* 検証データの精度（Validation Accuracy）は、エポック12で頭打ちになっています。これは、モデルが学習データに過剰に適合し始めた（過学習）兆候であるため、改善の余地として**Early Stopping**の導入を検討します。

---

## 💡 環境構築の手順

### 必要な環境
- Python 3.9+
- TensorFlow, Keras, OpenCV

### 実行方法
以下のコマンドで必要なライブラリをインストール後、学習済みモデル（`model.h5`）を使って推論を実行できます。

```bash
pip install -r requirements.txt
python infer.py --image_path ./test_image.jpg
