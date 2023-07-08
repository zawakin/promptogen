# コンセプト

## モジュール化

PrompGen は、Pythonオブジェクトとテキスト文字列の間の変換を行うプロセスとLLMとの通信を行うプロセスを分離しています。

このモジュラーな設計は、LLMが変わったり進化したりしても、PromptGenのコアな機能に影響を与えることなく、変化に適応しやすくなっています。

!!! note "モジュール化とは"

    ソフトウェア設計におけるモジュール化とは、システムをより小さく、管理しやすく、互いに相互作用できる独立したコンポーネント（モジュール）に分割することを指します。このアプローチの主な利点は以下の通りです。

    1. 独立性: 各モジュールは特定のタスクを独立して処理します。これにより、一つのモジュールを変更しても他のモジュールに影響を及ぼさないため、新しい機能を追加したり、更新したりする際の潜在的なリスクや問題を最小限に抑えることができます。

    2. 再利用性: モジュールは通常、再利用可能な設計となっています。これは同じモジュールがシステムの異なる部分や他のシステムでも使用できることを意味します。これにより時間を節約し、コードの重複を減らすことができます。

    3. メンテナンス: 各モジュールは特定のタスクを処理するので、理解、更新、デバッグ、テストが容易になります。また、それぞれのモジュールは別々のチームや個々人によって開発やメンテナンスが行われることも可能です。

## ライブラリの小規模化

PromptGen では、ライブラリを小さく保つために、Pythonオブジェクトとテキスト文字列の間の変換に焦点を当てています。LLMと直接やり取りするロジックを含まないことで、ライブラリは軽量かつ柔軟に保たれ、他のシステムとの統合やLLMの将来の変更や進化に対応するのが容易になります。

!!! note "ライブラリの小規模化のメリットとは"
    小さなライブラリの利点には以下のようなものがあります。

    1. 効率性: より小さなコードベースは理解、デバッグ、テスト、メンテナンスが容易です。
    2. シンプルさ: 単一の明確な目的を持つライブラリは、使いやすく、他のシステムの部分との予期しない副作用や競合を引き起こす可能性が低いです。
    3. 速度: 一般的に、小さなライブラリはより速くロードされ、実行されます。これにより全体的な時間と計算資源が節約されます。