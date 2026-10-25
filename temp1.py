from replay.batch_processor import BatchProcessor

processor = BatchProcessor()

objects = [1, 2, 3]

for i in range(6):

    result = processor.process(True, objects)

    print(result)

processor.process(False, [])

print("Done")