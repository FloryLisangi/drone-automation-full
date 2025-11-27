# Jetson Deployment & TensorRT Notes

- Export YOLO model to ONNX with `ultralytics`:
  `yolo export model=yolov8n.pt format=onnx`
- Convert ONNX to TensorRT:
  `trtexec --onnx=model.onnx --saveEngine=model.trt --fp16`
- Use Jetson's `nvrtc` and `tensorrt` runtime for inference.
- Use swap file and monitor thermal throttling. Use a fan for sustained inference.
