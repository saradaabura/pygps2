# Versuin 3,0
**���������[�N�����Ȃ�����**
- del���g�p���Ċ֐��̏������I�������Ƃ��ɕϐ����Ȃ����悤�ɂ����B
- gc���W���[�����g�p���ă������̉�����s���悤�ɂ����B
- ToDo�ɂ�������͋@�\��؂�ւ��ł���悤�ɂ����B
**������analyze_nmea_date�����s����Ə��������**

���\�[�X�����Ȃ��f�o�C�X�ł��g�p���₷���Ȃ����B

# Version 2.9
**�`�F�b�N�T���̋@�\��ǉ�**
- �e�Z���e���X���`�F�b�N�T���ɂ�茟�؂���@�\��ǉ�
��parse_nmea_sentences�ŏ��������ہA�`�F�b�N�T�������؂���悤�ɂȂ����B

����̓`�F�b�N�T�����؂�L���ɂ��邩�ǂ�����I���ł���悤�ɂ���\��B

# Version 2.8
**RMC��o�ܓx�ϊ��֐��̕ύX**
### RMC
- cpython������mktime�̃G���[����@cpython�ł�micropython�Ɠ����悤�Ɏg�p�\
### �o�ܓx�ϊ��֐�
- cpython��Decimal���g�p����悤�ɕύX�B

## �ǂ�������������micropython��cpython�ŏ�����ύX����悤�ɂ��Ă���B
����ɂ��Acpython���ł����肵�ē��삷��悤�ɂȂ����B
# Version 2.7
**decimal�֐���p����issues#2������**
�g�p�������C�u����
- micropython-decimal-number
https://github.com/mpy-dev/micropython-decimal-number/tree/main
THANK YOU!
lat��lon�͏�������O��str()�ŕ�����ɕϊ�����K�v������B����͂��̏������֐��ɑg�ݍ��ޗ\��B

float(str())�ɂ��ĉ��Z���s���ƁA���x�������邽�߂Ȃ�ׂ��Astr�ŕێ�����悤�ɂ���B

# Version 2.6

**�p�^�[���ɂȂ��f�[�^�̏���**

2.5�ȑO��patterns�ɂȂ��f�[�^�͏�������Ȃ��������A2.6�ȍ~�͏��������悤�ɂȂ����B

�������ꂽ�f�[�^��pygps2.parse_nmea_sentences()��Other�ɕ��ނ����Bpygps2.analyze_nmea_data()�ł͏�������Ȃ��B

# Version 2.5
**DHV ZDA TXT�ǉ�**
- ��̓Z���e���X�̒ǉ�
**FIX���Ă��Ȃ��Ƃ��̎�����2000/01/01�ɂȂ�܂���**
- time��mktime�G���[����̂���
# Version 2.4
**RMC�ύX**
- RMC�Ɍo�x����v�Z�������[�J��������ǉ�
���t�̕ύX�ɑΉ�

# Version 2.3
**GST��͊֐��ǉ�**
- GST�Z���e���X�̉�͊֐���ǉ�
# Version 2.2
**�q���̃f���A���o���h�ɂ��J�E���g�d���̉���**
GNSS�̃Z���e���X����2��ȏ㓯��PRN�����o����Ă��J�E���g���Ȃ��悤�ɂ����B

�܂����S�ł͂Ȃ����A�ꕔ�̃Z���e���X�ɑ΂��Ă͑Ή����Ă���B

����m�F
- AT6668
- AT6558
# Version 2.1
**GSV��͊֐��ύX**
- �q�����ʎq��ǉ�

GSV�Z���e���X�̐擪2�����ڂ���4�����ڂ��擾

��������ʎq�Ƃ��Ď�����"type"�ɒǉ�����悤�ɂ���

```��
$BDGSV "type":"BD"
$GPGSV "type":"GP"
$GAGSV "type":"GA"
$GLGSV "type":"GL"
$GNGSV "type":"GN"
$GQGSV "type":"GQ"
$GBGSV "type":"GB"
```
SBAS�ɂ��Ă͑Ή����Ă��Ȃ�

$GPGSV�̒��ɂ���QZSS���̃f�[�^��GP�Ƃ��ď��������B

���̂܂܂̏o�͂ł��邽�߁A�g�p���郂�W���[���ɂ���ăv���O������ύX����K�v������B

# Version 2.0
�쐬