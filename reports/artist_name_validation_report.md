# Artist Name Validation Report

Rejects awards, institutions, locations, sentence fragments, and navigation text.

- Input biographies: 122
- Valid biographies: 27
- Rejected biographies: 95
- Input profiles: 69
- Valid profiles: 12
- Rejected profiles: 57

## Valid Biographies

- 千葉智江 — Pinpoint Gallery — known_good
- 飯野和好 — Pinpoint Gallery — known_good
- つじにぬき — Pinpoint Gallery — known_good
- Charles Pears — Royal Institute of Painters in Water Colours — known_good
- Ronald Benham RBA NEAC — Royal Institute of Painters in Water Colours — known_good
- Charles Pears — Mall Galleries Open Exhibitions — known_good
- Ronald Benham RBA NEAC — Mall Galleries Open Exhibitions — known_good
- Charles Pears — Pastel Society Open Exhibition — known_good
- Ronald Benham RBA NEAC — Pastel Society Open Exhibition — known_good
- Andrew Pledge’s Hidden Gems — Royal Institute of Painters in Water Colours — en_person_pattern
- Catherine Beale’s — Royal Institute of Painters in Water Colours — en_person_pattern
- Grahame Booth — Royal Institute of Painters in Water Colours — known_good
- Andrew Graham-Dixon — Royal Institute of Painters in Water Colours — known_good
- Zhang Hongbin — Royal Institute of Painters in Water Colours — known_good
- Michael Harrison — Royal Institute of Painters in Water Colours — known_good
- Andrew Pledge’s Hidden Gems — Mall Galleries Open Exhibitions — en_person_pattern
- Catherine Beale’s — Mall Galleries Open Exhibitions — en_person_pattern
- Grahame Booth — Mall Galleries Open Exhibitions — known_good
- Andrew Graham-Dixon — Mall Galleries Open Exhibitions — known_good
- Zhang Hongbin — Mall Galleries Open Exhibitions — known_good
- Michael Harrison — Mall Galleries Open Exhibitions — known_good
- Andrew Pledge’s Hidden Gems — Pastel Society Open Exhibition — en_person_pattern
- Catherine Beale’s — Pastel Society Open Exhibition — en_person_pattern
- Grahame Booth — Pastel Society Open Exhibition — known_good
- Andrew Graham-Dixon — Pastel Society Open Exhibition — known_good
- Zhang Hongbin — Pastel Society Open Exhibition — known_good
- Michael Harrison — Pastel Society Open Exhibition — known_good

## Rejection Reasons

- reject_exact: 118
- starts:The: 6
- sentence_fragment_period: 4
- starts:Marine Artists: 4
- contains:Art Commissions: 4
- contains:Art Consultancy: 4
- contains:Arts Education: 4
- starts:Young Artist: 4
- starts:Art: 2
- no_person_pattern: 2

## Sample Rejections

- Bristol. The — reject_exact
- Bristol. The — reject_exact
- Bristol. The — reject_exact
- ピンポイント絵本コンペの — reject_exact
- Baltic Exchange. Including — reject_exact
- NCI. The Baltic — reject_exact
- The RSMA — reject_exact
- Lorraine Abraham. The — sentence_fragment_period
- Robert. Value — reject_exact
- Simon. Value — reject_exact
- Baltic Exchange. Including — reject_exact
- NCI. The Baltic — reject_exact
- The RSMA — reject_exact
- Lorraine Abraham. The — sentence_fragment_period
- Robert. Value — reject_exact
- Simon. Value — reject_exact
- Baltic Exchange. Including — reject_exact
- NCI. The Baltic — reject_exact
- The RSMA — reject_exact
- Lorraine Abraham. The — sentence_fragment_period
- Robert. Value — reject_exact
- Simon. Value — reject_exact
- アマ問わず — reject_exact
- Central London — reject_exact
- British Artists. Charity — reject_exact
- British Artists — reject_exact
- The RBA — reject_exact
- Marine Artists — starts:Marine Artists
- Queen Elizabeth II — reject_exact
- The Artist September — reject_exact
- The Natural Eye — reject_exact
- The Birdwatch — reject_exact
- Swarovski Optik Artist — reject_exact
- Art Commissions — contains:Art Commissions
- Art Consultancy — contains:Art Consultancy
- Arts Education — contains:Arts Education
- Her Royal Highness The — reject_exact
- British Artists CEO Tom — reject_exact
- Portrait Painters President Anthony — reject_exact
- Chinese Year — reject_exact