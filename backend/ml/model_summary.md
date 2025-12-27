# Model Training Summary

## Crop Prediction Model
**After Regularization Training:**
- Test Accuracy: 99.55%
- Average Confidence: 91.71% ✓ (much better than 99.77%)
- Max Confidence: 100% (still some edge cases)
- 100% predictions: reduced significantly
- 95%+ predictions: 250 out of 441 test samples

**Regularization Applied:**
- max_depth=10 (limited tree depth)
- min_samples_split=12 (require more samples to split)
- min_samples_leaf=5 (require more samples in leaves)
- max_features='sqrt' (limit features per split)

**Result:** Much improved! Average confidence is now realistic at 91.71%

## Fertilizer Recommendation Model
- Test Accuracy: 95.00% ✓
- Average Confidence: 81.67% ✓
- Max Confidence: 91.51% ✓
- 100% predictions: 0 ✓ (Perfect!)

## Summary
Both models now have realistic confidence scores. The fertilizer model is perfect with no 100% predictions. The crop model is much improved with average confidence of 91.71%, though some edge cases still show high confidence (which is acceptable for very clear-cut predictions).
