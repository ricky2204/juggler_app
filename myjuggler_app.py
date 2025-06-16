import math
from scipy.stats import binom
import streamlit as st # Streamlitをインポート

# 二項分布の確率を計算する関数 (変更なし)
def binomial_probability(n, k, p):
    if k < 0 or k > n:
        nCk = 0
    else:
        nCk = math.comb(n, k)
    probability = nCk * (p ** k) * ((1 - p) ** (n - k))
    return probability

# マイジャグラーVのブドウ確率（理論値） (変更なし)
grape_probabilities_theoretical = {
    "設定1": 1 / 5.90,
    "設定2": 1 / 5.85,
    "設定3": 1 / 5.80,
    "設定4": 1 / 5.78,
    "設定5": 1 / 5.76,
    "設定6": 1 / 5.66,
}

# Streamlitアプリのタイトル
st.title("マイジャグラー設定判別ツール")
st.write("総ゲーム数とブドウ出現回数を入力して、設定の事後確率を推測します。")

# ユーザー入力部分をStreamlitウィジェットに変更
# st.number_inputを使うと、数値入力フィールドを作成できる
observed_games = st.number_input("総ゲーム数を入力してください", min_value=1, value=2000, step=100)
observed_grapes = st.number_input("ブドウの出現回数を入力してください", min_value=0, value=345, step=10)

# 計算実行ボタン
if st.button("計算する"):
    if observed_grapes > observed_games:
        st.error("ブドウ出現回数は総ゲーム数を超えることはできません！")
    else:
        st.write("--- 観測データ ---")
        st.write(f"総ゲーム数: {observed_games} G")
        st.write(f"ブドウ出現回数: {observed_grapes} 回")
        if observed_games > 0: # 0割りを防ぐ
            st.write(f"実測ブドウ確率: {observed_grapes / observed_games:.4f}")
        else:
            st.write("実測ブドウ確率: N/A (総ゲーム数が0のため)")

        # 各設定におけるブドウ出現の尤度（likelihood）を計算
        st.write("\n--- 各設定でのブドウ出現の尤度 ---")
        likelihoods = {}
        for setting, p_grape in grape_probabilities_theoretical.items():
            likelihood = binom.pmf(observed_grapes, observed_games, p_grape)
            likelihoods[setting] = likelihood
            st.write(f"{setting} の尤度: {likelihood:.10e}")

        # 事前確率 (今回は固定値とするが、ユーザー入力にすることも可能)
        prior_probabilities = {
            "設定1": 1/6, "設定2": 1/6, "設定3": 1/6,
            "設定4": 1/6, "設定5": 1/6, "設定6": 1/6,
        }

        # 周辺尤度（エビデンス）の計算
        evidence = 0
        for setting in likelihoods:
            evidence += likelihoods[setting] * prior_probabilities[setting]

        # 事後確率（Posterior Probability）の計算
        st.write("\n--- 各設定である事後確率 ---")
        posterior_probabilities = {}
        if evidence > 0: # 0割りを防ぐ
            for setting in likelihoods:
                posterior = (likelihoods[setting] * prior_probabilities[setting]) / evidence
                posterior_probabilities[setting] = posterior
                st.write(f"{setting} である確率: {posterior:.2%}")

            # 最も確率が高い設定を特定
            most_likely_setting = max(posterior_probabilities, key=posterior_probabilities.get)
            st.success(f"最も可能性が高い設定は: {most_likely_setting}") # 成功メッセージとして表示
        else:
            st.warning("計算に必要な情報が不足しているか、極めて稀なケースです。")