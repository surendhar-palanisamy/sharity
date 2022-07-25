from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .blockchain import *
from .models import *
from node.models import *
from .algorithm import *
import datetime


@receiver(post_save, sender=User)
def profile_creation(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print(instance)


@receiver(post_save, sender=Payment)
def Blockchain_creation(sender, instance, created, **kwargs):
   
    #validation
    all_blocks = Block.objects.all()
    count = all_blocks.count()
    Node_blocks =Node_block.objects.all()
    Node_block_count=Node_blocks.count()
    print('Block count',count)
    print("Node_block_count", Node_block_count)
    if count < Node_block_count:
        all_blocks.delete()
        for data in Node_blocks:
            Block.objects.create(
            payment_header=data.payment_header, current_hash=data.current_hash, previous_hash=data.previous_hash, sender=data.sender, receiver=data.receiver, cash=data.cash, nonce=data.nonce, date_created=data.date_created)
    previous_block_number = 0
    current_block_number = 1

    
    for data in all_blocks:
        if current_block_number < count:
            current_block_previous_hash = all_blocks[current_block_number].previous_hash
            previous_block = all_blocks[previous_block_number]
            loop_previous_block_hash = validator(previous_block)
            if current_block_previous_hash != loop_previous_block_hash:
                previous_block_payment_header = previous_block.payment_header
                previous_block.sender = str(
                    previous_block_payment_header.sender_profile)
                previous_block.receiver = str(
                    previous_block_payment_header.receiver_profile)
                previous_block.cash = str(
                    previous_block_payment_header.cash)
                previous_block.date_created = str(
                    previous_block_payment_header.date_created)
                previous_block.save()
            current_block_number = current_block_number + 1
            previous_block_number = previous_block_number + 1

    #creation
    if created:
        last_object = Block.objects.last()
        if last_object is None:
            previous_hash = '0000000000000000000000000000000000000000000000000000000000000000'
        else:
            previous_hash = last_object.current_hash

        transactions = Payment.objects.last()
        sender = transactions.sender_profile
        receiver = transactions.receiver_profile
        cash = transactions.cash
        time_data = datetime.datetime.now()
        transactions.date_created = str(time_data)
        transactions.save()
        transaction_data = str(sender)+str(receiver)+str(cash)

        current_hash, nonce = mine(transaction_data, previous_hash, time_data)
        Block.objects.create(
            payment_header=transactions, current_hash=current_hash, previous_hash=previous_hash, sender=transactions.sender_profile, receiver=transactions.receiver_profile, cash=transactions.cash, nonce=nonce, date_created=str(time_data))
        Node_block.objects.create(
            payment_header=transactions, current_hash=current_hash, previous_hash=previous_hash, sender=transactions.sender_profile, receiver=transactions.receiver_profile, cash=transactions.cash, nonce=nonce, date_created=str(time_data))
        print('Transaction id', transactions.id,
              transactions.sender_profile, transactions.receiver_profile)
    #post_delete_after_fill
    #post_sort
       
       
        algo()
    

@receiver(post_save, sender=Post)
def Algo_sort(sender, instance, created, **kwargs):
    if created:
        algo()


