from recbole.trainer import Trainer


def train(config, model_class, data_list):

    tr_data, val_data, te_data = data_list

    model = model_class(config, tr_data.dataset).to(config['device'])
    trainer = Trainer(config, model)

    print("==== train start ====")
    best_valid_score, best_valid_result = trainer.fit(train_data=tr_data, valid_data=val_data)

    print("==== train end! ====")
    print(f"best valid score & result: {best_valid_score}, {best_valid_result}")

    print("==== evaluation start ====")
    test_result = trainer.evaluate(te_data)

    print(f"test_result: {test_result}")
