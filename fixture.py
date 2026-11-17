mock_api_response = {
    "paper_title": "Attention Is All You Need",
    "overall_rigor_score": 9,
    "executive_summary": (
        "The paper demonstrates exceptional evidential transparency. Nearly all architectural and performance "
        "claims are directly substantiated by quantitative benchmarks, ablation studies in Table 3, and "
        "training cost comparisons in Table 2."
    ),
    "claims": [
        {
            "id": "C1",
            "claim_text": "The Transformer model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over existing best results by over 2 BLEU.",
            "claim_location": "Abstract / Page 1",
            "evidence_status": "STRONG_INTERNAL",
            "evidence_quote": "On the WMT 2014 English-to-German translation task, the big transformer model outperforms the best previously reported models (including ensembles) by more than 2.0 BLEU, establishing a new state-of-the-art BLEU score of 28.4.",
            "evidence_location": "Section 6.1, Table 2 / Page 8",
            "audit_note": "Directly backed by exact quantitative benchmark metrics and comparative baselines reported in Table 2.",
        },
        {
            "id": "C2",
            "claim_text": "Self-attention layers are faster than recurrent layers when the sequence length n is smaller than the representation dimensionality d.",
            "claim_location": "Section 4 / Page 6",
            "evidence_status": "STRONG_INTERNAL",
            "evidence_quote": "In terms of computational complexity, self-attention layers are faster than recurrent layers when the sequence length n is smaller than the representation dimensionality d, which is most often the case with sentence representations.",
            "evidence_location": "Section 4, Table 1 / Page 6",
            "audit_note": "Substantiated mathematically via asymptotic complexity per layer O(n^2 * d) vs O(n * d^2) in Table 1.",
        },
        {
            "id": "C3",
            "claim_text": "Residual connections and layer normalization are employed around each sub-layer to stabilize deep network training.",
            "claim_location": "Section 3.1 / Page 3",
            "evidence_status": "EXTERNAL_CITATION",
            "evidence_quote": "We employ a residual connection [11] around each of the two sub-layers, followed by layer normalization [1].",
            "evidence_location": "Section 3.1 / Page 3",
            "audit_note": "Relies on foundational external literature ([11] He et al., [1] Ba et al.) for standard architectural components rather than re-proving them.",
        },
    ],
}
