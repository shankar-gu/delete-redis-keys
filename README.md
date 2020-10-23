# Delete Redis keys

Redis Enterprise CRDB (Active-Active) databases cannot execute multi-key operations with keys across different hash slots. In this context, UNLINK with multiple keys from a SCAN is not available. So iterating with SCAN and using a pipline to add UNLINK for each individual key is the next best, most efficient option. Tweak the batch size (SCAN and PIPELINE) and delay for optimal usage.
