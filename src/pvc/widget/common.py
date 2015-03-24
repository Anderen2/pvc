"""
Common Widgets Module

"""

import pvc.widget.menu
import pvc.widget.gauge
import pvc.widget.datastore
import pvc.widget.network
import pvc.widget.virtualmachine

__all__ = ['rename']


def rename(obj, dialog, text=''):
    """
    Rename a Managed Entity

    Args:
        obj    (vim.ManagedEntity): A Managed Entity
        dialog     (dialog.Dialog): A Dialog instance
        text                 (str): Text to display

    """
    code, new_name = dialog.inputbox(
        title=obj.name,
        text=text,
        init=obj.name
    )

    if code in (dialog.CANCEL, dialog.ESC):
        return

    task = obj.Rename(newName=new_name)
    gauge = pvc.widget.gauge.TaskGauge(
        title=obj.name,
        text='Renaming {} to {} ...'.format(obj.name, new_name),
        dialog=dialog,
        task=task
    )

    gauge.display()

def network_menu(agent, dialog, obj, text=''):
    """
    A widget to display the networks by a Managed Entity

    Args:
        agent         (VConnector): A VConnector instance
        dialog     (dialog.Dailog): A Dialog instance
        obj    (vim.ManagedEntity): A Managed Entity
        text                 (str): Text to display

    """
    dialog.infobox(
        text='Retrieving information ...'
    )

    if not hasattr(obj, 'network'):
        dialog.msgbox(
            title=obj.name,
            text='Entity does not contain any networks'
        )
        return

    if not obj.network:
        dialog.msgbox(
            title=obj.name,
            text='No networks found for this managed entity'
        )
        return

    items = [
        pvc.widget.menu.MenuItem(
            tag=network.name,
            description='Accessible' if network.summary.accessible else 'Not Accessible',
            on_select=pvc.widget.network.NetworkWidget,
            on_select_args=(agent, dialog, network)
        ) for network in obj.network
    ]

    menu = pvc.widget.menu.Menu(
        title=obj.name,
        text=text,
        items=items,
        dialog=dialog
    )

    menu.display()

def virtual_machine_menu(agent, dialog, obj, text=''):
    """
    A widget to display the VMs contained within a Managed Entity, e.g.
    HostSystem, ClusterComputeResource, Datastore, etc.

    Args:
        agent         (VConnector): A VConnector instance
        dialog     (dialog.Dailog): A Dialog instance
        obj    (vim.ManagedEntity): A Managed Entity
        text                 (str): Text to display

    """
    dialog.infobox(
        title=obj.name,
        text='Retrieving information ...'
    )

    if not hasattr(obj, 'vm'):
        dialog.msgbox(
            title=obj.name,
            text='Entity does not contain any Virtual Machines'
        )
        return

    if not obj.vm:
        dialog.msgbox(
            title=obj.name,
            text='No virtual machines found for this managed entity'
        )
        return

    items = [
        pvc.widget.menu.MenuItem(
            tag=vm.name,
            description=vm.runtime.powerState,
            on_select=pvc.widget.virtualmachine.VirtualMachineWidget,
            on_select_args=(agent, dialog, vm)
        ) for vm in obj.vm
    ]

    menu = pvc.widget.menu.Menu(
        title=obj.name,
        text=text,
        items=items,
        dialog=dialog
    )

    menu.display()

def datastore_menu(agent, dialog, obj, text=''):
    """
    A widget to get all Datastores used by a managed entity, e.g.
    HostSystem, VirtualMachine, Cluster, etc.

    Args:
        agent         (VConnector): A VConnector instance
        dialog     (dialog.Dailog): A Dialog instance
        obj    (vim.ManagedEntity): A Managed Entity
        text                 (str): Text to display

    """
    dialog.infobox(
        text='Retrieving information ...'
    )

    if not hasattr(obj, 'datastore'):
        dialog.msgbox(
            title=obj.name,
            text='Entity does not have any datastores'
        )
        return

    if not obj.datastore:
        dialog.msgbox(
            title=obj.name,
            text='No datastores found for this managed entity'
        )
        return

    items = [
        pvc.widget.menu.MenuItem(
            tag=dsname,
            description='Accessible' if ds.summary.accessible else 'Not Accessible',
            on_select=pvc.widget.datastore.DatastoreWidget,
            on_select_args=(agent, dialog, ds)
        ) for ds in obj.datastore
    ]

    menu = pvc.widget.menu.Menu(
        title=obj.name,
        text=text,
        items=items,
        dialog=dialog
    )

    menu.display()